import re
from typing import Optional
from .utils import QueryError, Constraints


class Parser:
    def __init__(self):
        self.under_pattern = r"(?:under|less than)\s*\$?(\d+(?:\.\d{1,2})?)(?:\s*dollars?)?"
        self.over_dollars_pattern = r"over\s*\$?(\d+(?:\.\d{1,2})?)(?:\s*dollars?)?"
        self.between_pattern = r"between\s*\$?(\d+(?:\.\d{1,2})?)\s*(?:and|to|-)\s*\$?(\d+(?:\.\d{1,2})?)(?:\s*dollars?)?"
        
        self.over_reviews_pattern = r"over\s*(\d+(?:,\d{3})*)\s*reviews?"
        self.good_reviews_pattern = r"good reviews"
        
        self.shipping_patterns = [
            r"prime shipping",
            r"2-day shipping",
            r"free shipping",
            r"prime"
        ]
        
        self.rating_pattern = r"(?:at least|min(?:imum)?)\s*(\d+(?:\.\d)?)\s*stars?"
        
        self.filler_phrases = [
            r"\bfind\b",
            r"\blooking for\b",
            r"\bshow me\b",
            r"\bi want\b",
            r"\bsomething\b",
            r"\bwith\b",
            r"\band\b",
            r"\bthat has\b",
            r"\bwhich has\b",
            r"\bit should have\b"
        ]
        
        self.known_categories = {
            "coffee maker": "coffee maker",
            "headphones": "headphones",
            "camera lenses": "camera lenses",
            "water bottle": "water bottle",
            "wireless mouse": "wireless mouse",
            "gaming laptop": "gaming laptop",
            "smart watch": "smart watch",
            "portable speaker": "portable speaker"
        }


    def _remove_pattern(self, text: str, pattern: str) -> str:
        cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', cleaned).strip()


    def _clean_text(self, text: str) -> str:
        for phrase in self.filler_phrases:
            text = self._remove_pattern(text, phrase)
        
        text = re.sub(r'[^\w\s]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()


    def _extract_category(self, text: str) -> Optional[str]:
        if not text:
            return None
            
        for keyword, category in self.known_categories.items():
            if keyword in text:
                return category
        
        article_match = re.search(r"(?:a|an)\s+([a-z\s]+?)$", text)
        if article_match:
            return article_match.group(1).strip()
        
        return text.strip()


    def parse(self, query: str, existing_constraints: Optional[Constraints] = None) -> Constraints:
        """
        Parse a user query to extract product search criteria.
        
        Args:
            query: The user's query string
            existing_constraints: Optional dictionary of existing constraints from the shopping agent
            
        Returns:
            Dict containing parsed constraints, merged with existing constraints
        """
        if not query or not query.strip():
            raise QueryError("Your query is empty. Please specify what you're looking for.")
        
        result: Constraints = {
            "category": None,
            "min_price": None,
            "max_price": None,
            "prime_required": False,
            "min_rating": None,
            "min_reviews": None
        }
        
        if existing_constraints:
            result.update(existing_constraints)
        
        query = query.lower().strip()
        working_query = query
        
        over_dollars_match = re.search(self.over_dollars_pattern, working_query)
        if over_dollars_match:
            result["min_price"] = float(over_dollars_match.group(1))
            working_query = self._remove_pattern(working_query, self.over_dollars_pattern)
        
        under_price_match = re.search(self.under_pattern, working_query)
        if under_price_match:
            result["max_price"] = float(under_price_match.group(1))
            working_query = self._remove_pattern(working_query, self.under_pattern)
        
        between_price_match = re.search(self.between_pattern, working_query)
        if between_price_match:
            result["min_price"] = float(between_price_match.group(1))
            result["max_price"] = float(between_price_match.group(2))
            working_query = self._remove_pattern(working_query, self.between_pattern)
        
        over_reviews_match = re.search(self.over_reviews_pattern, working_query)
        if over_reviews_match:
            review_count = over_reviews_match.group(1).replace(',', '')
            result["min_reviews"] = int(review_count)
            working_query = self._remove_pattern(working_query, self.over_reviews_pattern)
        elif re.search(self.good_reviews_pattern, working_query):
            result["min_reviews"] = 100
            working_query = self._remove_pattern(working_query, self.good_reviews_pattern)
        
        for pattern in self.shipping_patterns:
            if re.search(pattern, working_query):
                result["prime_required"] = True
                working_query = self._remove_pattern(working_query, pattern)
                break
        
        rating_match = re.search(self.rating_pattern, working_query)
        if rating_match:
            result["min_rating"] = float(rating_match.group(1))
            working_query = self._remove_pattern(working_query, self.rating_pattern)
        
        working_query = self._clean_text(working_query)
        if working_query:
            new_category = self._extract_category(working_query)
            if new_category:
                result["category"] = new_category
        
        if not result["category"] and not (existing_constraints and existing_constraints.get("category")):
            raise QueryError("Your query is too broad or incomplete. Please specify what product you're looking for and any requirements.")
        
        return result
