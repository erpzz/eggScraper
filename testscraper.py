from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import requests 
import time
from datetime import date
from selenium.webdriver.common.by import By


def eggScraper():
    try:
        storeName = input("Enter store name: ").lower()
        time.sleep(1)
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        storeState = input("Enter state initials: ").upper()
        while storeState not in states:
            print("Invalid state. Enter a valid state.")
            storeState = input("Enter state initials: ").upper()
        
        time.sleep(1)
        print(f"Welcome to {storeName} in {storeState}")
        time.sleep(1)
        print("Please wait a moment..")
        time.sleep(1)
        print("...")
        time.sleep(1)
        options = Options()
        #options.add_argument('--headless')
        chromeDriverPath = '/usr/bin/chromedriver'
        options.add_experimental_option("detach", True)
        chromeService = ChromeService()
        driver = webdriver.Chrome(service=chromeService, options=options)
        url = ('https://www.target.com/s?searchTerm=eggs+12+ct&tref=typeahead%7Cterm%7Ceggs+12+ct%7C%7C%7C')
        driver.get(url)
        
        print('Website connecting, scraper waking up...')
        time.sleep(5)

        print("Parsing to begin.")
        htmlContent = driver.page_source
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-test="product-title"]'))
        )
        
        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(htmlContent)
        with open('page.html', 'r', encoding='utf-8') as f:
            htmlContent = f.read()
        soup = BeautifulSoup(htmlContent, 'html.parser')
        locations = []
        locationSelector = soup.select('span[class="styles__StyledNameSpan-sc-ujzcd7-6 fyQsDI"]')
        for location in locationSelector:
            locationName = location.get_text().strip().lower()
            locations.append(locationName)
        zipCodes = []
        zipCodes.append(locations[0])
        s = zipCodes[0]
        zipCode = s.split()[-1]
        town = locations[1]
        selectors = soup.select('a[data-test="product-title"]')
        productTypes = []
        TypesSelector = soup.select('a[class="styles__StyledLink-sc-vpsldm-0 cnZxgy h-text-md h-text-grayDark"]')
        
        for types in TypesSelector:
            productType = types.get_text().strip()
            productTypes.append(productType)
        print(productTypes)
        c = 0
        non_egg_keywords = ['timer', 'color', 'dye', 'easter', 'hershey', 'candy']
        titlesList = []
        for productTitles in selectors:
            productName = productTitles.get_text().strip().lower()
            if 'egg' in productName and not any(keyword in productName for keyword in non_egg_keywords):
                c = c + 1
                # print(f'Listed egg result {c}: {productName}')
                titlesList.append(productName)
            else:
                print(f'Skipped non-egg result: {productName}')
        print(titlesList)
        print(f"The number of products is : {c  }")
        priceSelectors = soup.select('span[data-test="current-price"]')
        time.sleep(2)
        prices = []
        for productPrices in priceSelectors:
            productPrice = productPrices.get_text().strip().lower()
            prices.append(productPrice)
        print(prices)
    
    
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {type(e).__name__}: {e}")

    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")


    finally:
        print("Closing Connection...")
        driver.quit()
        print("Connection closed.")

eggScraper()
