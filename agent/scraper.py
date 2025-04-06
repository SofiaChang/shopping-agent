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

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

class Scraper:
    def __init__(self, headless: bool = True):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.driver = self._create_driver(headless)
        self.raw_html = ""
        self.parsed_products: List[Product] = []
        self.last_request_time = 0
        self.requests_per_minute = 15
        self.min_delay = 2  
        self.max_delay = 6


    def _create_driver(self, headless: bool) -> webdriver.Chrome:
        try:
            options = Options()
            if headless:
                options.add_argument("--headless")
            
            user_agent = random.choice(UA_POOL)
            options.add_argument(f"--user-agent={user_agent}")    
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-blink-features=AutomationControlled")
            
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
        try:
            self._enforce_rate_limit()            
            search_url = f"{base_url}/s?k={search_term.replace(' ', '+')}"
            
            if constraints:
                if constraints.get('min_price') is not None:
                    search_url += f"&rh=p_36%3A{int(constraints['min_price'] * 100)}-"
                if constraints.get('max_price') is not None:
                    if constraints.get('min_price') is None:
                        search_url += "&rh=p_36%3A-"
                    search_url += f"{int(constraints['max_price'] * 100)}"
                if constraints.get('prime_required'):
                    search_url += "&rh=p_85%3A2470955011"
            
            logger.info(f"Navigating to {search_url}")
            self.driver.get(search_url)
            self._random_delay()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-component-type='s-search-result']")
                )
            )
            
            self.raw_html = self.driver.page_source
            self._extract_products(results_to_fetch)
            
            return self.parsed_products
            
        except TimeoutException:
            logger.error("Timeout waiting for search results")
            raise Exception("Search timed out. Please try again later.")
        except Exception as e:
            logger.error(f"Error during search and scrape: {str(e)}")
            raise


    def _extract_products(self, results_to_fetch: int) -> None:
        try:
            product_containers = self.driver.find_elements(
                By.XPATH, 
                "//div[@data-component-type='s-search-result']"
            )[:results_to_fetch]
            
            self.parsed_products = []
            for container in product_containers:
                try:
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
                    
                except Exception as e:
                    logger.warning(f"Error extracting product: {str(e)}")
                    continue
                    
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
