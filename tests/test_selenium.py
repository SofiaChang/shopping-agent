import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    # 1. Initialize the Chrome WebDriver
    # If ChromeDriver is on your system PATH or in the same folder, this should work directly:
    driver = webdriver.Chrome()

    # 2. Navigate to a test site (e.g., Google)
    test_url = "https://www.google.com"
    print(f"Navigating to: {test_url}")
    driver.get(test_url)

    # 3. Wait a bit (to see it in action)
    time.sleep(3)

    # 4. Check the page title
    print("Page title is:", driver.title)

    # 5. Close the browser
    driver.quit()
    print("Test complete! Browser closed.")

if __name__ == "__main__":
    main()
