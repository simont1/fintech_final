#functions go here

stocks =[
    {"symbol": "GOOGL", "price": 1253.22},    
    {"symbol": "MSFT", "price": 141.53}
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
    # {"symbol": "", "price": }
]


def price_range(money):
    ret_arr = []
    for stock in stocks:
        if money > stock["price"]:
            shares_available = money / stock["price"]
            ret_arr.append({stock["symbol"]: str(int(shares_available)) + " shares purchasable"})
            # ret_arr.append(stock["symbol"] + " " + str(int(shares_available)) + " shares purchasable")
    return ret_arr
            
price_range(5000)