#functions go here
import csv
import matplotlib.pyplot as plt

stocks = [
]

# with open('static/sp500.csv', newline='') as csvfile:
with open('app/static/sp500.csv', newline='') as csvfile:
     lines = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in lines:
        #  print(row)
        #  print(row[0] + ", " + row[1] + "'s closing price is " + row[2])
        temp = int(row[4])
        # print(temp)
        if (temp > 1000000000):
            temp = str(int(temp / 1000000000)) + " B"
        elif (temp > 1000000):
            temp = str(int(temp / 1000000)) + " M"
        else:
            temp = str(temp)
        
        stocks.append({"symbol": row[0], "name": row[1], "price": float(row[2]), "market_cap": temp, "PE": float(row[5]), "yearly_change": float(row[3])})

# stocks =[
    # {"symbol": "GOOGL", "price": 1253.22},    
    # {"symbol": "MSFT", "price": 141.53}
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
# ]


def price_range(money):
    # ret_arr = stocks
    ret_arr = []
    for stock in stocks:
        if money > stock["price"]:
            shares_available = money / stock["price"]
            ret_arr.append(stock)
            ret_arr[ret_arr.index(stock)]["shares"] = str(int(shares_available)) + " shares purchasable"
            # ret_arr[ctr]["shares"] =  str(int(shares_available)) + " shares purchasable"
            # ret_arr.append(stock["symbol"] + " " + str(int(shares_available)) + " shares purchasable")
        # else:
            # ret_arr.remove(stock)
    return ret_arr
            
# print(price_range(5000))
# for i in stocks:
    # print(i)
