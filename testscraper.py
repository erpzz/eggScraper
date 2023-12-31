from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import requests
import time

def eggScraper():
    try:
        options = Options()
        chromeDriverPath = '/usr/bin/chromedriver'
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        chromeService = ChromeService(executable_path=chromeDriverPath)
        driver = webdriver.Chrome(service=chromeService, options=options)
        url = ('https://www.target.com/s?searchTerm=eggs+12+ct&tref=typeahead%7Cterm%7Ceggs+12+ct%7C%7C%7Chistory')
        driver.get(url)

        
        print('Website found, attempting to connect...')
        time.sleep(1)
        #print(response.status_code)
        htmlContent = driver.page_source
        time.sleep(5)
        soup = BeautifulSoup(htmlContent, 'html.parser')
        print("Parsing to begin.")

      # Find all div elements with class 'styles__Truncate-sc-1wcknu2-0 iZqUcy'
      #  truncate_divs = soup.find_all('div', attrs={"data-test": "product-grid"})

        # Print the number of found div elements
       # print(f"Number of div elements with data-test: product-grid': {len(truncate_divs)}")

        # Filter div elements with an 'a' child element with data-test='product-title'
       # 

        # Print the number of found product titles
        
    # print(soup.prettify())

       # productTitles = soup.select('a[data-test="product-grid"] a[data-test="product-table"]')
       # 
       # for title in truncate_divs:
            
        productTitles = soup.select('div[data-test="product-grid"] a[data-test="product-title"]')
        print("aria-label")
        print(f"Number of a elements with data-test: product-title': {len(productTitles)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


    finally:
        print("Closing Connection")
        driver.quit()
eggScraper()