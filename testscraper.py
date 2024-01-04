from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import requests 
import time


def eggScraper():
    try:
        options = Options()
        options.add_argument('--headless')
        chromeDriverPath = '/usr/bin/chromedriver'
        options.add_experimental_option("detach", True)
        chromeService = ChromeService(executable_path=chromeDriverPath)
        driver = webdriver.Chrome(service=chromeService, options=options)
        url = ('https://www.target.com/s?searchTerm=eggs+12+ct&tref=typeahead%7Cterm%7Ceggs+12+ct%7C%7C%7Chistory')
        driver.get(url)
        print('Website connecting, scraper waking up...')
        time.sleep(1)
       # print(f"Response code: {response.status_code}")
        print("Parsing to begin.")
        
        productGrid = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located('div[data-test="product-grid"]')
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        truncate_divs = soup.select('div[data-test="product-grid"]')

        print(f"Number of div elements with data-test: product-grid': {len(truncate_divs)}")
        productTitles = productGrid.find_elements(By.CSS_SELECTOR, 'a[data-test="product-title"]')
        for productTitle in productTitles:
            print(productTitle.text.strip())
            
            
        #time.sleep(2)

        # Filter div elements with an 'a' child element with data-test='product-title'
       # 

        # Print the number of found product titles
        
    # print(soup.prettify())

       # productTitles = soup.select('a[data-test="product-grid"] a[data-test="product-table"]')
       # 
        
       # print(f"Number of a elements with data-test: product-title': {len(productTitles)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


    finally:
        print("Closing Connection")
        #driver.quit()
eggScraper()
