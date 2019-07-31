import sqlite3

from datetime import datetime

import csv

def init2():
    DB_FILE = "stocks.db"
    
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    with open("sp5000.csv") as csvfile:
        command = "CREATE TABLE IF NOT EXISTS stocks(symbol TEXT, name TEXT, price REAL, market_cap REAL, PE REAL, yearly_change REAL, sector TEXT)"
        c.execute(command)
        
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print (row)
            # c.execute("INSERT INTO stocks (symbol, name, price, yearly_change, market_cap, PE, sector) VALUES ('" + row['symbol'] + "','" + row['name'] + "','" + row['price'] + "','" + row['yearly_change'] + "','" + row['market_cap'] + "','" + row['PE'] + "','" + row['sector']"');")
            c.execute("INSERT INTO stocks VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(row['symbols'], row['names'], row['prices'], row['market_caps'], row['PEs'], row['yearly_changes'], row['sectors']))
    db.commit()
    db.close()
    
init2()

def browse():
    DB_FILE = "stocks.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    command = "SELECT * FROM stocks"
    c.execute(command)
    
    
    for i in c:
        print(i)
        
    db.commit()
    db.close()
        
browse()

# DB_FILE="profiles.db"

# def init():
#     db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
#     c = db.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS userDirectory(username TEXT, password TEXT)")
#     c.execute("INSERT INTO userDirectory VALUES('admin','admin')")
#     db.commit()
#     db.close()
    
# def isUser(user):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("SELECT username FROM userDirectory WHERE username = '{0}'".format(user))
#     name = c.fetchone()
#     db.commit()
#     db.close()
#     if name != None and len(name) > 0:
#         return True
#     return False

# init()
# print(isUser('admin'))

# def getPw(user):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("SELECT password FROM userDirectory WHERE username = '{0}'".format(user))
#     x = c.fetchone()
#     db.commit()
#     db.close()
#     return x[0]
    
# def register(user, pw):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()

#     c.execute("INSERT INTO userDirectory VALUES('{0}','{1}')".format(user,pw))
#     #Adds user to the userDirectory db
    
#     c.execute("CREATE TABLE IF NOT EXISTS '{0}' (stock TEXT, shares INTEGER, purchase_date TEXT)".format(user))
#     #Creates the new db named after the user for their profile

#     c.execute("CREATE TABLE IF NOT EXISTS '{0}' (option TEXT, stock TEXT, shares INTEGER, option_date TEXT)".format(user+"History"))
#     #Creates the new db recording the user's trading history
    
#     #Initial Add-ons :)
#     c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(user, "CREATED", 0, datetime.utcnow()))
#     c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(user+"History", "CREATED", 0, "CREATED", datetime.utcnow()))

#     db.commit()
#     db.close()
    
    
# # def buy_stock(user, stock, shares):
# #     db = sqlite3.connect(DB_FILE, check_same_thread=False)
# #     c = db.cursor()
# #     if stock_exists(user, stock):
# #         #Code block here
# #     else:
# #         c.execute("INSERT INTO '{0}' VALUES('{1}', '{2}', '{3}')".format(user, stock, shares, datetime.utcnow()))
# #         c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(user+"History", "BUY", stock, shares, datetime.utcnow()))
    
# #     db.commit()
# #     db.close()
    
    
# def stock_exists(user, stock):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("SELECT stock FROM '{0}' WHERE stock = '{1}'".format(user, stock)) #tests to see if stock is in portfoli
#     name = c.fetchone()
#     db.commit()
#     db.close()
#     if name != None and len(name) > 0:
#         return True
#     return False

# def sell_stock(user, stock, shares):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("SELECT stock FROM '{0}' WHERE stock = '{1}'".format(user, stock)) #tests to see if stock is in portfoli
#     name = c.fetchone()
#     if name != None and len(name) > 0:
#         c.execute("SELECT stock FROM '{0}' WHERE stock = '{1}'".format(user, stock))
#         c.execute("INSERT INTO '{0}' VALUES('{1}', '{2}', '{3}')".format(user, stock, shares, datetime.utcnow()))
#         c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(user+"History", "SELL", stock, shares, datetime.utcnow()))
    
#     db.commit()
#     db.close()


# def clear(user):
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("DELETE FROM userDirectory WHERE username = '{0}'".format(user))
#     db.commit()
#     db.close()
    
# def clearAll():
#     db = sqlite3.connect(DB_FILE, check_same_thread=False)
#     c = db.cursor()
#     c.execute("DROP TABLE userDirectory")
#     db.commit()
#     db.close()
    
# # clearAll()
# # clear('admin')
# # register('Simon', 'Simon')
# # register('Amulya', 'Amulya')

