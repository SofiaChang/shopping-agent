import json
import logging
import time
import random
from typing import List, Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .utils import Constraints, Product
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class Scraper:
    def __init__(self, headless: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.current_user_agent = random.choice(USER_AGENTS)
        self.logger.info(f"Initializing scraper with user agent: {self.current_user_agent}")
        
        self.driver = self._create_driver(headless)
        self.raw_html = ""
        self.parsed_products: List[Product] = []
        self.last_request_time = 0
        self.requests_per_minute = 15
        self.min_delay = 3
        self.max_delay = 7


    def _create_driver(self, headless: bool) -> webdriver.Chrome:
        try:
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            options.add_argument(f"--user-agent={self.current_user_agent}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
            return driver
        except Exception as e:
            self.logger.error(f"Error creating WebDriver: {str(e)}")
            raise


    def _rotate_user_agent(self):
        new_user_agent = random.choice([ua for ua in USER_AGENTS if ua != self.current_user_agent])
        self.current_user_agent = new_user_agent
        self.logger.info(f"Rotating to new user agent: {self.current_user_agent}")
        
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.current_user_agent})


    def _enforce_rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        min_time_between_requests = 60 / self.requests_per_minute
        
        if time_since_last_request < min_time_between_requests:
            sleep_time = min_time_between_requests - time_since_last_request
            self.logger.info(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


    def _random_delay(self):
        delay = random.uniform(self.min_delay, self.max_delay)
        self.logger.debug(f"Adding random delay of {delay:.2f} seconds")
        time.sleep(delay)


    def search_and_scrape(self, search_term: str, constraints: Constraints = None, results_to_fetch: int = 5, base_url: str = "https://www.amazon.com") -> List[Product]:
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    self._rotate_user_agent()
                
                self._enforce_rate_limit()
                
                search_url = f"{base_url}/s?k={search_term.replace(' ', '+')}"
                logger.info(f"Searching Amazon for: {search_term} (attempt {attempt + 1}/{max_retries})")
                logger.info(f"Using URL: {search_url}")
                logger.info(f"Using user agent: {self.current_user_agent}")
                
                logger.info("Navigating to search page...")
                self.driver.get(search_url)
                logger.info("Page navigation complete, adding random delay...")
                self._random_delay()
                
                try:
                    logger.info("Waiting for page to be fully loaded...")
                    WebDriverWait(self.driver, 20).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    logger.info("Page loaded successfully")
                    
                    logger.info("Waiting for search results or no results message...")
                    WebDriverWait(self.driver, 20).until(
                        lambda driver: (
                            len(driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")) > 0 or
                            len(driver.find_elements(By.XPATH, "//div[contains(text(), 'No results for')]")) > 0
                        )
                    )
                    logger.info("Search results or no results message found")
                    
                    no_results = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'No results for')]")
                    if no_results:
                        logger.info("No results found for search term")
                        return []
                    
                    logger.info("Waiting for product prices to load...")
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']//span[@class='a-price']"))
                    )
                    logger.info("Product prices loaded successfully")
                    
                except TimeoutException as e:
                    logger.warning(f"Timeout waiting for page elements (attempt {attempt + 1}): {str(e)}")
                    logger.warning(f"Current URL: {self.driver.current_url}")
                    logger.warning(f"Page source length: {len(self.driver.page_source)}")
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    raise Exception("Search timed out. Please try again later.")
                
                logger.info(f"Extracting up to {results_to_fetch} products...")
                products = self._extract_products(results_to_fetch)
                
                if not products:
                    logger.warning("No products extracted from search results")
                    logger.warning(f"Number of product containers found: {len(self.driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]'))}")
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    return []
                
                logger.info(f"Successfully extracted {len(products)} products")
                return products
                
            except Exception as e:
                logger.error(f"Error during search (attempt {attempt + 1}): {str(e)}")
                logger.error(f"Current URL: {self.driver.current_url}")
                logger.error(f"Page source length: {len(self.driver.page_source)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                raise Exception(f"Search failed after {max_retries} attempts. Please try again later.")
        
        return []


    def _extract_products(self, results_to_fetch: int) -> List[Product]:
        try:
            logger.info("Finding product containers...")
            product_containers = self.driver.find_elements(
                By.XPATH, 
                "//div[@data-component-type='s-search-result']"
            )[:results_to_fetch]
            logger.info(f"Found {len(product_containers)} product containers")
            
            self.parsed_products = []
            for i, container in enumerate(product_containers, 1):
                try:
                    logger.info(f"Processing product {i}/{len(product_containers)}")
                    product_data: Product = {
                        'title': self._extract_text(container, ".//h2//span"),
                        'price': self._extract_price(container),
                        'rating': self._extract_rating(container),
                        'review_count': self._extract_review_count(container),
                        'prime': self._has_prime(container),
                        'url': self._extract_url(container),
                        'thumbnail': self._extract_thumbnail(container)
                    }
                    
                    if product_data['title']:
                        self.parsed_products.append(product_data)
                        logger.info(f"Successfully extracted product: {product_data['title']}")
                    else:
                        logger.warning(f"Product {i} has no title, skipping")
                    
                except Exception as e:
                    logger.warning(f"Error extracting product {i}: {str(e)}")
                    continue
                    
            logger.info(f"Successfully processed {len(self.parsed_products)} products")
            return self.parsed_products
                    
        except Exception as e:
            logger.error(f"Error in product extraction: {str(e)}")
            raise


    def _extract_text(self, container, xpath: str) -> Optional[str]:
        try:
            element = container.find_element(By.XPATH, xpath)
            return element.text.strip()
        except:
            return None


    def _extract_price(self, container) -> Optional[float]:
        try:
            whole_price = self._extract_text(container, ".//span[@class='a-price-whole']")
            fraction_price = self._extract_text(container, ".//span[@class='a-price-fraction']")
            
            if whole_price and fraction_price:
                return float(f"{whole_price.replace(',', '')}.{fraction_price}")
        except:
            return None


    def _extract_rating(self, container) -> Optional[float]:
        try:
            rating_elem = container.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
            rating_text = rating_elem.get_attribute('innerHTML')
            if 'out of 5 stars' in rating_text:
                return float(rating_text.split(' out of ')[0])
        except:
            return None


    def _extract_review_count(self, container) -> Optional[int]:
        try:
            review_elem = container.find_element(
                By.XPATH,
                ".//a[contains(@aria-label, 'ratings')]/span[contains(@class,'a-size-base s-underline-text')]"
            )
            review_text = review_elem.text
            if review_text:
                review_count = ''.join(filter(str.isdigit, review_text))
                if review_count:
                    return int(review_count)
        except:
            return None


    def _extract_url(self, container) -> Optional[str]:
        try:
            return container.find_element(By.XPATH, ".//a[@class='a-link-normal s-line-clamp-4 s-link-style a-text-normal']").get_attribute('href')
        except:
            return None


    def _extract_thumbnail(self, container) -> Optional[str]:
        try:
            return container.find_element(By.XPATH, ".//img[@class='s-image']").get_attribute('src')
        except:
            return None


    def _has_prime(self, container) -> bool:
        try:
            container.find_element(By.XPATH, ".//i[@aria-label='Amazon Prime']")
            return True
        except:
            return False


    def close(self) -> None:
        try:
            self.driver.quit()
            logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")
            raise
