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
import sqlite3 
from dataclasses import dataclass, field
import re

@dataclass 
class Eggs:
    type: str
    price: float
    store: str
    entryDate: date = field(default_factory=date.today())
@dataclass
class Store:
    storeName: str
    town: str
    state: str
    zipCode: str

class DataBaseManager:
    def __init__(self, db_Name):
        self.conn = sqlite3.connect(db_Name)

    def createEggTable(self):
        eggTableQuery = ''' 
        
        CREATE TABLE IF NOT EXISTS Eggs(
            EggID INTEGER PRIMARY KEY AUTOINCREMENT,
            Type TEXT,
            Price REAL, 
            Store TEXT, 
            EntryDate DATE
        )'''
        self.conn.execute(eggTableQuery)
        print("Table Created successfully.")
    
    def saveEggs(self, egg):
        cur = self.conn.cursor()
        insertEggQuery = '''
        
        INSERT INTO Eggs (Type, Price, Store, EntryDate)
            VALUES(?, ?, ?, ?)
        '''
        try: 
            cur.execute(insertEggQuery,(egg.type, egg.price, egg.store, egg.entryDate))
            self.conn.commit()

        except Exception as e:
            print(f'Error committing data: {e}')
        
        else:
            print("Commit Successful.")
        
        finally:
            cur.close()
   

    def createStoreTable(self):
        storeTableQuery = ''' 
        
        CREATE TABLE IF NOT EXISTS Stores(
            StoreID INTEGER PRIMARY KEY AUTOINCREMENT,
            StoreName TEXT,
            Town TEXT,
            State TEXT,
            ZipCode TEXT
        )
        '''
        self.conn.execute(storeTableQuery)
        print("Table Created Sucessfully.")
    def addTownColumn(self):
        addTownQuery = ''' 
        ALTER TABLE Stores
        ADD COLUMN Town TEXT
        '''
        self.conn.execute(addTownQuery)
        print("Town column added successfully.")
    
    def addStateColumn(self):
        addStateQuery = ''' 
        ALTER TABLE Stores
        ADD COLUMN State TEXT
        '''
        self.conn.execute(addStateQuery)
        print("State column added successfully.")

    def addZipCodeColumn(self):
        addZipCodeQuery = ''' 
        ALTER TABLE Stores
        ADD COLUMN ZipCode TEXT
        '''
        self.conn.execute(addZipCodeQuery)
        print("ZipCode column added successfully.")
    def saveStore(self, store):
        cur = self.conn.cursor()
        insertStoreQuery = ''' 
            INSERT INTO Stores(StoreName, Town, State, ZipCode)
            VALUES(?, ?, ?, ?)
            
        '''      
        try:
            cur.execute(insertStoreQuery,(store.storeName, store.town, store.state, store.zipCode))
            self.conn.commit()

        except Exception as e:
            print(f'Error committing data: {e}')
        
        else:
            print("Commit Successful.")
        
        finally:
            cur.close()
            self.conn.close()

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
        time.sleep(1)
        selectors = soup.select('a[data-test="product-title"]')
        productTypes = []
        TypesSelector = soup.select('a[class="styles__StyledLink-sc-vpsldm-0 cnZxgy h-text-md h-text-grayDark"]')
       
        non_egg_keywords = ['timer', 'color', 'dye', 'easter', 'hershey', 'candy', 'mint']
        for types in TypesSelector:
            productType = types.get_text().strip().lower()
            if not any(keyword in productType for keyword in non_egg_keywords):
                productTypes.append(productType)
        print(f"Welcome to {storeName} in {town}, {storeState}, {zipCode}.")
        time.sleep(2)
        print(productTypes)
        priceSelectors = soup.select('span[data-test="current-price"]')
        time.sleep(2)
       
        
        c = 0
        titlesList = []
        prices = []

        for productTitles, productPrices in zip(selectors, priceSelectors):
            productName = productTitles.get_text().strip().lower()
            productPrice = productPrices.get_text().strip().lower()

            if 'egg' in productName and not any(keyword in productName for keyword in non_egg_keywords):
                c = c + 1
                titlesList.append(productName)
                match = re.search(r'\d+\.\d+', productPrice)
                if match:
                    purePrice = float(match.group())
                    prices.append(purePrice)
            else:
                print(f'Skipped non-egg result: {productName}')

        print(titlesList)
        print(prices)
        eggsList = []
        for productType, price, productName in zip(productTypes, prices, titlesList):
            egg = Eggs(type=productType, price=price, store=storeName, entryDate=date.today())
            eggsList.append(egg)
        for egg in eggsList:
            print(egg)

        # Database connection    
        dbManager = DataBaseManager('eggs.db')
        dbManager.createEggTable()
        dbManager.createStoreTable()
        # dbManager.addTownColumn()
        #dbManager.addStateColumn()
        #dbManager.addZipCodeColumn()
        for egg in eggsList:
            dbManager.saveEggs(egg)

        store = Store(storeName=storeName, town=locationName, state=storeState, zipCode=zipCode)
        dbManager.saveStore(store)
  #  for e in 
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {type(e).__name__}: {e}")

    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")


    finally:
        print("Closing Connection...")
        driver.quit()
        print("Connection closed.")
        

eggScraper()
