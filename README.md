# Amazon Shopping Assistant

This project implements an Amazon Shopping Assistant that parses user queries (e.g. "Find me a coffee maker under $100 with prime shipping"), scrapes Amazon using Selenium, and returns filtered & ranked products. It supports multi-turn conversation, partial refinements ("under $50 now," "make it prime," etc.), and a "new search" feature.

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Technical Requirements](#technical-requirements)
4. [Setup & Installation](#setup--installation)
5. [Usage](#usage)
6. [Features & Capabilities](#features--capabilities)
7. [Known Limitations & Future Improvements](#known-limitations--future-improvements)
8. [Critical Design Choices](#critical-design-choices)

## Overview

The Amazon Shopping Assistant is a Python-based application that helps users find products on Amazon based on natural language queries. It uses a combination of natural language processing, web scraping, and constraint-based filtering to provide relevant product recommendations.

Key features include:
- Natural language query parsing
- Multi-turn conversation support
- Partial query refinements
- Product filtering and ranking
- Anti-detection measures for web scraping
- User-friendly web interface

## Project Structure

```
shopping-agent/
├── agent/
│   ├── __init__.py
│   ├── parser.py          # Query parsing and constraint extraction
│   ├── scraper.py         # Amazon product scraping
│   └── shopping_agent.py  # Main agent logic
├── utils.py               # Shared types and utilities
├── main.py                # To run independently of web interface
├── app.py                 # Streamlit web interface
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Technical Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver
- Required Python packages (see requirements.txt):
  - streamlit
  - selenium
  - webdriver-manager
  - typing-extensions

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd shopping-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install ChromeDriver:
   ```bash
   pip install webdriver-manager
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter your search query in the text input field (e.g., "Find me a coffee maker under $100 with prime shipping")

4. View the results and use the "New Search" button to start a fresh search

## Features & Capabilities

### Query Parsing
- Extracts product categories, price ranges, and other constraints
- Supports partial refinements (e.g., "under $50 now", "make it prime")
- Maintains context between queries

### Product Scraping
- Extracts product details including:
  - Title and price
  - Ratings and review counts
  - Prime eligibility
  - Product URLs and thumbnails
- Implements anti-detection measures:
  - User agent rotation
  - Random delays between requests
  - Rate limiting

### Multi-turn Conversation
- Maintains conversation history
- Supports incremental refinements
- Allows starting new searches

### Web Interface
- Clean, responsive design
- Product cards with images and details
- Clickable product links
- Search history display

## Known Limitations & Future Improvements

### Current Limitations
- Limited to first page of Amazon search results
- Basic natural language processing
- No support for complex queries (e.g., "cheaper than X but better rated than Y")
- Rate limiting may cause delays

### Planned Improvements
- [ ] Support for multiple pages of results
- [ ] Enhanced natural language processing
- [ ] Support for more complex queries
- [ ] Product comparison features
- [ ] Price history tracking
- [ ] User preferences and saved searches
- [ ] Mobile-responsive design improvements
- [ ] Integration with Amazon API (if available)

## Critical Design Choices

### Architecture
- **Modular Design**: The system is split into distinct components (parser, scraper, agent) for better maintainability and testing
- **Type Safety**: Uses TypedDict for data structures to ensure type consistency across components
- **Separation of Concerns**: Clear boundaries between web scraping, parsing, and business logic

### Query Parsing Strategy
- **Incremental Parsing**: Supports partial refinements by maintaining existing constraints
- **Constraint Merging**: New constraints are merged with existing ones, with more restrictive values taking precedence
- **Natural Language Patterns**: Uses regex patterns to identify common shopping-related phrases
- **Context Preservation**: Maintains category context between queries unless explicitly changed

### Product Ranking & Filtering
- **Two-Stage Process**: 
  1. Strict filtering based on hard constraints (price, prime, etc.)
  2. Ranking of remaining products based on ratings and review counts
- **Priority Order**:
  Products are ranked using a tuple-based sorting approach where criteria are evaluated in strict priority order:
  1. Rating (highest first): Primary factor for quality assessment
  2. Review Count (most reviews first): Secondary factor indicating product popularity and reliability
  3. Price (lowest first): Tertiary factor for cost-effectiveness
  4. Prime Status (Prime products first): Final tiebreaker when other factors are equal
  
  This approach ensures that:
  - High-quality products (good ratings) are always prioritized
  - Well-reviewed products are preferred over those with few reviews
  - Price becomes a factor only when ratings and reviews are comparable
  - Prime status serves as a final differentiator
- **Flexible Matching**: Products that don't meet all constraints are shown as "other suggestions"

### Web Scraping Approach
- **Anti-Detection Measures**:
  - User agent rotation
  - Random delays (2-6 seconds)
  - Rate limiting (20 requests/minute)
  - WebDriver fingerprint masking
- **Robust Extraction**:
  - Safe element extraction with fallbacks
  - Graceful handling of missing data
  - Comprehensive error logging

### State Management
- **Session-Based**: Uses Streamlit's session state for conversation history
- **Constraint Persistence**: Maintains constraints between queries for natural refinement
- **Clean Reset**: "New Search" feature completely resets the conversation state

### Error Handling
- **Graceful Degradation**: Continues operation even if some products fail to parse
- **Informative Messages**: Clear error messages for rate limits and timeouts
- **Logging**: Comprehensive logging at different severity levels

### Interface Design
- **Responsive Layout**: Two-column design for product display
- **Progressive Disclosure**: Shows essential info first, details on demand
- **Visual Hierarchy**: Clear distinction between matching products and suggestions to products that didn't fully meet the constraints, giving users more options
- **Interactive Elements**: Clickable product links and thumbnails

These design choices were made to balance:
- User experience vs. technical complexity
- Scraping efficiency vs. detection avoidance
- Strict filtering vs. flexible suggestions
- Immediate results vs. comprehensive data
