#functions go here
import csv
# import matplotlib.pyplot as plt

stocks = [
]

# with open('static/sp500.csv', newline='') as csvfile:
# with open('app/static/sp500.csv', newline='') as csvfile:
#      lines = csv.reader(csvfile, delimiter=',', quotechar='|')
#      for row in lines:
#         #  print(row)
#         #  print(row[0] + ", " + row[1] + "'s closing price is " + row[2])
#         temp = int(row[4])
#         # print(temp)
#         if (temp > 1000000000):
#             temp = str(int(temp / 1000000000)) + " B"
#         elif (temp > 1000000):
#             temp = str(int(temp / 1000000)) + " M"
#         else:
#             temp = str(temp)
        
#         stocks.append({"symbol": row[0], "name": row[1], "price": float(row[2]), "market_cap": temp, "PE": float(row[5]), "yearly_change": float(row[3])})

#uncomment below line out when you are working with terminal
# with open('static/sp5000.csv', newline='') as csvfile:
#comment this out when you are just working with terminal
with open('app/static/sp5000.csv', newline='') as csvfile:
    lines = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in lines:
        temp = int(row[4])
        if (temp > 1000000000):
            temp = str(int(temp / 1000000000)) + " B"
        elif(temp > 1000000):
            temp = str(int(temp / 1000000)) + " M"
        else:
            temp = str(temp)
        stocks.append({"symbol": row[0], "name": row[1], "price": float(row[2]), "market_cap": temp, "PE": float(row[5]), "yearly_change": float(row[3]), "sector": row[6]})

# stocks =[
    # {"symbol": "GOOGL", "price": 1253.22},    
    # {"symbol": "MSFT", "price": 141.53}
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
# ]

def go_through(symbol):
    for row in stocks:
        if symbol == row['symbol']:
            return True
    return False
        
# print(go_through("AAPL"))


def filter_criteria(money, volatility, sector):
    # ret_arr = stocks
    ret_arr = []
    for stock in stocks:
        if (money > stock["price"] and 
        ((abs(stock["yearly_change"]) < 20 and str(volatility) == "low") or 
        (abs(stock["yearly_change"]) >= 20 and abs(stock["yearly_change"]) <= 50 and str(volatility) == "medium") or
        (abs(stock["yearly_change"]) > 50 and str(volatility) == "high"))
        ):
            # print(len(sector))
            for x in range(len(sector)):
                if (sector[x] == stock["sector"]): 
                    shares_available = money / stock["price"]
                    ret_arr.append(stock)
                    ret_arr[ret_arr.index(stock)]["shares"] = str(int(shares_available)) + " shares purchasable"
            # ret_arr[ctr]["shares"] =  str(int(shares_available)) + " shares purchasable"
            # ret_arr.append(stock["symbol"] + " " + str(int(shares_available)) + " shares purchasable")
        # else:
            # ret_arr.remove(stock)
    return ret_arr

#use this to see price range, all data            
# print(price_range(5000))

#use this to see just stocks 
# for i in stocks:
    # print(i)

