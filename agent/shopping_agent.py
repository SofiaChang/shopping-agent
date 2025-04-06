import logging
from typing import List, Dict, Optional
from .parser import Parser
from .scraper import Scraper
from .utils import Product, Constraints, SearchResults, QueryError


class ShoppingAgent:
    def __init__(self, log_level: int = logging.INFO, enable_history: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        self.parser = Parser()
        self.scraper = None
        
        self.constraints: Constraints = {
            "category": None,
            "min_price": None,
            "max_price": None,
            "prime_required": False,
            "min_rating": None,
            "min_reviews": None
        }
        self.current_products = []
        self.history = [] if enable_history else None


    def _initialize_scraper(self, headless: bool = True) -> None:
        if self.scraper is None:
            self.scraper = Scraper(headless)
            self.logger.info("Initialized scraper")


    def _merge_constraints(self, new_constraints: Constraints) -> None:
        for key, value in new_constraints.items():
            if value is not None:
                self.constraints[key] = value
                self.logger.info(f"Updated constraint {key} to {value}")


    def _filter_products(self, products: List[Product], constraints: Constraints) -> List[Product]:
        matching_products = []
        other_products = []
        
        for product in products:
            missing_fields = [key for key in ['title', 'price', 'rating', 'review_count', 'prime', 'url', 'thumbnail'] 
                            if key not in product or product[key] is None]
            if missing_fields:
                other_products.append(product)
                continue
            
            satisfies_max_price_constraints = product.get('price', float('inf')) <= constraints['max_price'] if constraints.get('max_price') is not None else True
            satisfies_min_price_constraints = product.get('price', 0) >= constraints['min_price'] if constraints.get('min_price') is not None else True
            satisfies_rating_constraints = product.get('rating', 0.0) >= constraints['min_rating'] if constraints.get('min_rating') is not None else True
            satisfies_review_count_constraints = product.get('review_count', 0) >= constraints['min_reviews'] if constraints.get('min_reviews') is not None else True
            satisfies_prime_constraints = product.get('prime') if constraints.get('prime_required') else True

            if (satisfies_max_price_constraints
                and satisfies_min_price_constraints
                and satisfies_rating_constraints
                and satisfies_review_count_constraints
                and satisfies_prime_constraints):
                matching_products.append(product)
            else:
                other_products.append(product)    
            
            self.logger.debug(f"Product '{product.get('title', 'Unknown')}' \n Product details: {product} \n constraints check:")
            self.logger.debug(f"- Missing fields: {missing_fields}")
            self.logger.debug(f"- Price constraints: max={satisfies_max_price_constraints}, min={satisfies_min_price_constraints}")
            self.logger.debug(f"- Rating constraint: {satisfies_rating_constraints}")
            self.logger.debug(f"- Review count constraint: {satisfies_review_count_constraints}")
            self.logger.debug(f"- Prime constraint: {satisfies_prime_constraints}")

            
        self.logger.info(f"Filtered {len(products)} products:")
        self.logger.info(f"- Matching: {len(matching_products)}")
        self.logger.info(f"- Filtered out: {len(other_products)}")

                
        return matching_products, other_products


    def _rank_products(self, products: List[Product]) -> List[Product]:
        """Rank products based on multiple criteria in order of priority:
        1. Rating (highest first)
        2. Review count (most reviews first)
        3. Price (lowest first)
        4. Prime status (Prime products first when all else is equal)
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of products sorted by ranking criteria
        """
        self.logger.debug("Ranking products")


        def sort_key(product: Product) -> tuple:
            rating_sort = -product.get('rating', 0.0)            
            review_sort = -product.get('review_count', 0)
            price_sort = product.get('price', float('inf'))
            prime_sort = -int(product.get('prime', False))
            
            return (rating_sort, review_sort, price_sort, prime_sort)
            
        ranked = sorted(products, key=sort_key)
        self.logger.info(f"Ranked {len(ranked)} products")
        
        return ranked


    def handle_request(self, user_input: str, results_to_fetch: int = 10, headless: bool = True) -> SearchResults:
        """Handle a user shopping request.
        
        For each request:
        1. Parse new constraints from user input
        2. Merge with existing constraints
        3. Filter current products
        4. Re-scrape if needed (fewer than 3 matches)
        5. Rank and return results
        """
        self.logger.info(f"Handling request: {user_input}")
        
        try:
            new_constraints = self.parser.parse(user_input, self.constraints)
            self.logger.info(f"Parsed constraints: {new_constraints}")
            
            self._merge_constraints(new_constraints)
            self._initialize_scraper(headless)            
            matching_products, other_products = self._filter_products(
                self.current_products, 
                self.constraints
            )
            
            if len(matching_products) < 3:
                self.logger.info("Fewer than 3 matches, performing new scrape")
                self.current_products = self.scraper.search_and_scrape(
                    self.constraints["category"],
                    self.constraints,
                    results_to_fetch
                )
                matching_products, other_products = self._filter_products(
                    self.current_products,
                    self.constraints
                )
            ranked_products = self._rank_products(matching_products)
            
            if self.history is not None:
                self.history.append({
                    "input": user_input,
                    "constraints": dict(self.constraints),
                    "results": len(ranked_products)
                })
            
            return {
                "products": ranked_products,
                "other_products": other_products
            }
            
        except QueryError as e:
            self.logger.error(f"Query error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error handling request: {str(e)}", exc_info=True)
            raise


    def close(self) -> None:
        if self.scraper:
            self.scraper.close()
            self.logger.info("Closed scraper") 
