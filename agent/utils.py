from typing import TypedDict, Optional, List

class Product(TypedDict, total=False):
    title: str
    price: Optional[float]
    rating: Optional[float]
    review_count: Optional[int]
    prime: bool
    url: Optional[str]
    thumbnail: Optional[str]

class Constraints(TypedDict, total=False):
    category: Optional[str]
    min_price: Optional[float]
    max_price: Optional[float]
    prime_required: bool
    min_rating: Optional[float]
    min_reviews: Optional[int]

class SearchResults(TypedDict):
    products: List[Product]
    other_products: List[Product] 

class QueryError(Exception):
    pass
