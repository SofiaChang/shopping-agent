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
