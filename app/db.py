import sqlite3
import csv

def init():
    DB_FILE = "stocks.db"
    
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    with open("sp500.csv") as csvfile:
        # command = "CREATE TABLE stocks (symbol TEXT, name TEXT, price REAL, market_cap REAL, PE REAL, yearly_change REAL)"
        # c.execute(command)
        
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print (row)
            c.execute("INSERT INTO stocks (symbol, name, price, yearly_change, market_cap, PE) VALUES ('" + row['symbol'] + "','" + row['name'] + "','" + row['price'] + "','" + row['yearly_change'] + "','" + row['market_cap'] + "','" + row['PE'] + "');")
    
    db.commit()
    db.close()
    
init()