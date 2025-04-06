import pytest
from agent.parser import Parser, QueryError

@pytest.fixture
def parser():
    return Parser()

def test_known_categories(parser):
    """Test parsing queries with known categories."""
    test_cases = [
        ("Find me a coffee maker under $100", "coffee maker"),
        ("I want headphones with good reviews", "headphones"),
        ("Show me camera lenses with prime shipping", "camera lenses"),
        ("Looking for a water bottle between $10-$20", "water bottle"),
    ]
    
    for query, expected_category in test_cases:
        result = parser.parse(query)
        assert result['category'] == expected_category

def test_categories_with_articles(parser):
    """Test parsing queries with categories that include articles."""
    test_cases = [
        ("Find an ergonomic keyboard under $80", "ergonomic keyboard"),
        ("I want a wireless mouse with at least 4 stars", "wireless mouse"),
        ("Show me a gaming laptop with over 1000 reviews", "gaming laptop"),
        ("Looking for an external hard drive with prime shipping", "external hard drive"),
    ]
    
    for query, expected_category in test_cases:
        result = parser.parse(query)
        assert result['category'] == expected_category

def test_categories_without_articles(parser):
    """Test parsing queries with categories that don't include articles."""
    test_cases = [
        ("wireless earbuds under $50", "wireless earbuds"),
        ("mechanical keyboard with good reviews", "mechanical keyboard"),
        ("smart home device between $30-$50", "smart home device"),
    ]
    
    for query, expected_category in test_cases:
        result = parser.parse(query)
        assert result['category'] == expected_category

def test_complex_category_names(parser):
    """Test parsing queries with complex category names."""
    test_cases = [
        ("Find a noise-cancelling wireless headset under $200", "noise cancelling wireless headset"),
        ("I want a 4K ultra HD smart TV with prime shipping", "hd smart tv"),
        ("Looking for a portable Bluetooth speaker with good reviews", "portable bluetooth speaker"),
    ]
    
    for query, expected_category in test_cases:
        result = parser.parse(query)
        assert result['category'] == expected_category

def test_edge_cases(parser):
    """Test parsing queries with edge cases that should raise errors."""
    test_cases = [
        "Find something under $50",  # No category
        "Show me with prime shipping",  # No category
        "I want with good reviews",  # No category
        "",  # Empty query
        "   ",  # Whitespace only
    ]
    
    for query in test_cases:
        with pytest.raises(QueryError):
            parser.parse(query)

def test_price_constraints(parser):
    """Test parsing queries with various price constraints."""
    test_cases = [
        ("Find me a coffee maker under $100", {"min_price": None, "max_price": 100.0}),
        ("Looking for a water bottle between $10-$20", {"min_price": 10.0, "max_price": 20.0}),
        ("Show me products over $50", {"min_price": 50.0, "max_price": None}),
    ]
    
    for query, expected_prices in test_cases:
        result = parser.parse(query)
        assert result['min_price'] == expected_prices['min_price']
        assert result['max_price'] == expected_prices['max_price']

def test_rating_constraints(parser):
    """Test parsing queries with rating constraints."""
    test_cases = [
        ("Find me a product with at least 4 stars", {"min_rating": 4.0}),
        ("Show me items with good reviews", {"min_rating": 4.0}),
    ]
    
    for query, expected_rating in test_cases:
        result = parser.parse(query)
        assert result['min_rating'] == expected_rating['min_rating']

def test_prime_shipping(parser):
    """Test parsing queries with Prime shipping requirements."""
    test_cases = [
        ("Find me a product with prime shipping", {"prime_required": True}),
        ("Show me items with free shipping", {"prime_required": True}),
        ("Looking for something with regular shipping", {"prime_required": False}),
    ]
    
    for query, expected_prime in test_cases:
        result = parser.parse(query)
        assert result['prime_required'] == expected_prime['prime_required'] 