# Eric Paiz, December 28, 2023. Egg scraper tool 

import sqlite3 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup



class Eggs:
    def __init__(self, type, price, store, entryDate):
        self.type = type
        self.price = price
        self.store = store
        self.entryDate = entryDate

class Store:
    def __init__(self, storeName, town, state):
        self.storeName = storeName
        self.town = town
        self.state = state

class DataBaseManager:
    def __init__(self, db_Name):
        self.conn = sqlite3.connect(db_Name)

    def createTables(self):
        eggTableQuery = ''' 
            CREATE TABLE IF NOT EXISTS Eggs(
                eggID INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                price REAL, 
                store TEXT, 
                entryDate DATE
        '''
        self.conn.execute(eggTableQuery)
        print("Table Created successfully.")

    def saveEggs(self, eggs):
        cur = self.conn.cursor()
        insertEggQuery = '''
        
        INSERT INTO Eggs (type, price, store, entryDate)
            VALUES(?, ?, ?, ?)
         '''
        try: 
            cur.execute(insertEggQuery,(Eggs.type, Eggs.price, Eggs.store))
            self.conn.commit()

        except Exception as e:
            print(f'Error committing data: {e}')
        
        else:
            print("Commit Successful.")
        
        finally:
            cur.close()
            self.conn.close()
