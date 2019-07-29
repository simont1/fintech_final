#functions go here
import csv


stocks = [
]


with open('static/sp500.csv', newline='') as csvfile:
     lines = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in lines:
        #  print(row[0] + ", " + row[1] + "'s closing price is " + row[2])
         stocks.append({"symbol": row[0], "name": row[1], "close": float(row[2])})


# stocks =[
    # {"symbol": "GOOGL", "price": 1253.22},    
    # {"symbol": "MSFT", "price": 141.53}
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
# ]


def price_range(money):
    ret_arr = []
    for stock in stocks:
        if money > stock["close"]:
            shares_available = money / stock["close"]
            ret_arr.append({stock["symbol"]: str(int(shares_available)) + " shares purchasable"})
            # ret_arr.append(stock["symbol"] + " " + str(int(shares_available)) + " shares purchasable")
    return ret_arr
            
print(price_range(5000))