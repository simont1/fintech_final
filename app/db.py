import sqlite3

from datetime import datetime

# import csv

# def init2():
#     DB_FILE = "stocks.db"
    
#     db = sqlite3.connect(DB_FILE)
#     c = db.cursor()
    
#     with open("sp5000.csv") as csvfile:
#         command = "CREATE TABLE IF NOT EXISTS stocks(symbol TEXT, name TEXT, price REAL, market_cap REAL, PE REAL, yearly_change REAL, sector TEXT)"
#         c.execute(command)
        
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             print (row['sectors'])
#             # c.execute("INSERT INTO stocks (symbol, name, price, yearly_change, market_cap, PE, sector) VALUES ('" + row['symbol'] + "','" + row['name'] + "','" + row['price'] + "','" + row['yearly_change'] + "','" + row['market_cap'] + "','" + row['PE'] + "','" + row['sector']"');")
#             # c.execute("INSERT INTO stocks VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(row['symbols'], row['names'], row['prices'], row['market_caps'], row['PEs'], row['yearly_changes'], row['sectors']))
#     db.commit()
#     db.close()
    
# init2()

# def browse():
#     DB_FILE = "stocks.db"
#     db = sqlite3.connect(DB_FILE)
#     c = db.cursor()
    
#     command = "SELECT * FROM stocks"
#     c.execute(command)
    
    
#     for i in c:
#         print(i)
        
#     db.commit()
#     db.close()
        
# browse()

DB_FILE="profiles.db"


    
def isUser(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT username FROM userDirectory WHERE username = '{0}'".format(user))
    name = c.fetchone()
    db.commit()
    db.close()
    if name != None and len(name) > 0:
        return True
    return False

# print(isUser('admin'))

def getPw(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT password FROM userDirectory WHERE username = '{0}'".format(user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x[0]
    
def register(user, pw):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("INSERT INTO userDirectory VALUES('{0}','{1}')".format(user,pw))
    #Adds user to the userDirectory db
    
    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (stock TEXT, shares INTEGER, purchase_price REAL, purchase_date TEXT)".format(user))
    #Creates the new db named after the user for their profile

    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (option TEXT, stock TEXT, shares INTEGER, purchase_price REAL, option_date TEXT)".format(user+"History"))
    #Creates the new db recording the user's trading history
    
    #Initial Add-ons :)
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(user, "CREATED", 0, 0, datetime.now()))
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}', '{5}')".format(user+"History", "CREATED", 0, "CREATED", 0,  datetime.now()))

    db.commit()
    db.close()
    
def view_stocks(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM '{0}'".format(user))
    x = c.fetchall()
    retarr = []
    for i in x:
        if i != None:
            retarr.append({"stock": i[0], "shares": i[1], "purchase_price": i[2], "purchase_date": i[3]})
    return retarr
    
# view_stocks("Simon")
# print(view_stocks("Simon"))
    
def buy_stock(user, stock, shares, price):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO '{0}' VALUES('{1}', '{2}', '{3}', '{4}')".format(user, stock, shares, price, datetime.now()))
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}', '{5}')".format(user+"History", "BUY", stock, shares, price, datetime.now()))
    
    db.commit()
    db.close()
    
def buy_stock2(user, stock, shares, price): #If existing shares are in portfolio
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT shares FROM '{0}' WHERE stock = '{1}'".format(user, stock))
    num = c.fetchone()
    new_shares = int(num[0]) + shares
    c.execute("SELECT purchase_price FROM {0} WHERE stock = '{1}'".format(user, stock))
    old_purchase_price = c.fetchone()[0]
    old_investment = old_purchase_price * float(num[0])
    new_purchase_price = (old_investment + shares * price) / new_shares
    c.execute("UPDATE '{0}' SET shares = '{1}' where stock = '{2}'".format(user, new_shares, stock))
    c.execute("UPDATE '{0}' SET purchase_price = '{1}' where stock = '{2}'".format(user, new_purchase_price, stock))
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}', '{5}')".format(user+"History", "BUY", stock, shares, price, datetime.now()))
    db.commit()
    db.close()
    return True
    
# buy_stock2("Simon", "CREATED", 100, 15.24)


def stock_exists(user, stock):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT stock FROM '{0}' WHERE stock = '{1}'".format(user, stock)) #tests to see if stock is in portfolio
    name = c.fetchone()
    db.commit()
    db.close()
    if name != None and len(name) > 0:
        return True
    return False
    

def sell_stock(user, stock, shares, price):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT shares FROM '{0}' WHERE stock = '{1}'".format(user, stock))
    num = c.fetchone()
    if int(num[0]) == shares:
        c.execute("DELETE FROM '{0}' WHERE stock = '{1}'".format(user, stock))
    elif int(num[0]) < shares:
        return "You don't own that many shares, sale is invalid."
    else:
        new_shares = int(num[0]) - shares
        c.execute("UPDATE '{0}' SET shares = '{1}' WHERE stock = '{2}'".format(user, new_shares, stock))
        c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(user+"History", "SELL", stock, shares, datetime.now()))
    db.commit()
    db.close()


def clear(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DELETE FROM userDirectory WHERE username = '{0}'".format(user))
    c.execute("DROP TABLE '{0}'".format(user))
    c.execute("DROP TABLE '{0}'".format(user+"History"))
    db.commit()
    db.close()
    
def clearAll():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DROP TABLE userDirectory")
    db.commit()
    db.close()
    
def init():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()
    # clearAll()
    c.execute("CREATE TABLE IF NOT EXISTS userDirectory(username TEXT, password TEXT)")
    db.commit()
    db.close()

init()
# clearAll()
# clear('admin')
# register('Simon', 'Simon')
# clear('Simon')
# register('Amulya', 'Amulya')

