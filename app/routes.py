from app import app
from flask import render_template, request, redirect, flash
from app.models import model, formopener
from app import back, api, db


from os import urandom
app.secret_key = urandom(32)
session = {}

@app.route('/')
@app.route('/index')

def index():
    if 'user' in session:
        return render_template("index3.html")
    else:
        return render_template("index.html")
    
@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/auth', methods=["GET", "POST"])
def auth():
    data = request.form
    username = data['user']
    password = data['pass']
    
    #username and passwords match
    if db.isUser(username) and db.getPw(username) == password:
        session['user'] = username
        return redirect('/index')

    #username doesn't match
    elif db.isUser(username) == False:
        flash("Username or password not found")
        return render_template('login.html', error=True)

    #password doesn't match username
    elif db.getPw(username) != password:
        flash("Username or password not found")
        return render_template('login.html', error=True)
@app.route("/register", methods=["GET", "POST"])
def register():
    data = request.form
    print(data)
    username = data['Username']
    password = data['Password']
    confirm_password = data["Confirm_Password"]
    
    if len(username) == 0:
        flash("Username field cannot be left blank")
        return render_template('login.html', error=True)
    
    if len(password) == 0:
        flash("Password field cannot be left blank")
        return render_template('login.html', error=True)
    
    if password != confirm_password:
        flash("Passwords do not match")
        return render_template('login.html', error=True)
    
    if db.isUser(username):
        flash("user already exists")
        return render_template('login.html', error=True)
        
    elif db.isUser(username) == False:
        db.register(username, password)
        flash("Account successfully created")
        return render_template('login.html', success=True)

@app.route('/quiz')
def quiz():
    return render_template("quiz.1.html")
    
@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
    return redirect('/')
    
@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "GET":
        return "Nothing to see here! Go back."
    else:
        user_data = request.form
        if user_data["investment_amount"].isdigit():
            if 'volatility' in user_data:
                if len(user_data.getlist('sector')) > 0:
                    investment_amount = float(user_data["investment_amount"])
                    # print(investment_amount)
                    volatility = user_data["volatility"]
                    print(volatility)
                    sector = user_data.getlist('sector')
                    print(sector)
                    display = back.filter_criteria(investment_amount, volatility, sector)
                    # print(display)
                    # print(volatility)
                    return render_template("results.html", stocks = display)
                else:
                    flash("Please check off at least one sector option")
                return render_template("quiz.1.html", error = True)
            else:
                flash("Please check off one volatility option")
            return render_template("quiz.1.html", error = True)
        else:
            flash("Please enter a number for investment amount")
            return render_template("quiz.1.html", error = True)
            
    
@app.route('/individual', methods=["GET", "POST"])
def individual():
    if request.method == "GET":
        return "Nothing to see here! Go back."
    else:
        user_data = request.form
        labels = api.labels(user_data['symbol'])
        legend = "Daily data for the past year"
        values = api.values(user_data['symbol'])
        SMA = api.find_SMA(user_data['symbol'])
        info = api.find_stock(user_data['symbol'])
        # print(labels)
        # print(values)
        return render_template("individual.html", values = values, labels = labels, legend = legend, symbol = user_data['symbol'], SMA = SMA, info = info)
        
@app.route('/portfolio', methods=["GET", "POST"])
def portfolio():
        if 'user' in session:
            stock_portfolio = db.view_stocks(session["user"])
            stock_history = db.view_stocksHistory(session["user"])
            # print(stock_portfolio)
            return render_template('portfolio.html', stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
        else:
            flash('Not currently logged in')
            return redirect('/')
            
@app.route('/purchase', methods=["GET", "POST"])
def purchase():
    if 'user' in session:
        if request.method == "GET":
            return "Nothing to see here! Go back."
        else:
            user_data = request.form
            if user_data["shares"].isdigit():
                if back.go_through(user_data['symbol']):
                    if db.stock_exists(session['user'], user_data['symbol']):
                        price = api.find_stock(user_data['symbol'])["price"]
                        db.buy_stock2(session['user'], user_data['symbol'], int(user_data['shares']), price)
                        stock_portfolio = db.view_stocks(session["user"])
                        stock_history = db.view_stocksHistory(session["user"])
                        flash(user_data['symbol'] + " has been added to your portfolio!")
                        return render_template("portfolio.html", success = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
                    price = api.find_stock(user_data['symbol'])["price"]
                    db.buy_stock(session['user'], user_data['symbol'], user_data['shares'], price)
                    stock_portfolio = db.view_stocks(session["user"])
                    stock_history = db.view_stocksHistory(session["user"])
                    flash(user_data['symbol'] + " has been added to your portfolio!")
                    return render_template("portfolio.html", success = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
                else:
                    flash(user_data['symbol'] + " is not a purchaseable stock")
                    stock_portfolio = db.view_stocks(session["user"])
                    stock_history = db.view_stocksHistory(session["user"])
                    return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
            else:
                flash("Shares must be a number")
                stock_portfolio = db.view_stocks(session["user"])
                stock_history = db.view_stocksHistory(session["user"])
                return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
    else:
        flash("Not currently logged in")
        return redirect('/')
        
        
@app.route('/sell', methods=["GET", "POST"])
def sell():
    if 'user' in session:
        if request.method == "GET":
            return "Nothing to see here! Go back."
        else:
            user_data = request.form
            if user_data["shares"].isdigit():
                if back.go_through(user_data['symbol']):
                    if db.stock_exists(session['user'], user_data['symbol']):
                        if db.get_shares(session['user'], user_data['symbol']) > int(user_data['shares']):
                            price = api.find_stock(user_data['symbol'])["price"]
                            db.sell_stock(session['user'], user_data['symbol'], int(user_data['shares']), price)
                            stock_portfolio = db.view_stocks(session["user"])
                            stock_history = db.view_stocksHistory(session["user"])
                            flash("Sale was successful!")
                            return render_template("portfolio.html", success = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
                        else:
                            flash("You don't own that many shares")
                            stock_portfolio = db.view_stocks(session["user"])
                            stock_history = db.view_stocksHistory(session["user"])
                            return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
                    else:
                        flash("You do not own that stock")
                        stock_portfolio = db.view_stocks(session["user"])
                        stock_history = db.view_stocksHistory(session["user"])
                        return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
                else:
                    flash("Invalid stock. Stock is not tradeable")
                    stock_portfolio = db.view_stocks(session["user"])
                    stock_history = db.view_stocksHistory(session["user"])
                    return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
            else:
                flash("Number of shares must be a number")
                stock_portfolio = db.view_stocks(session["user"])
                stock_history = db.view_stocksHistory(session["user"])
                return render_template('portfolio.html', error = True, stock_portfolio = stock_portfolio, user = session['user'], stock_history = stock_history)
    else:
        flash("Must be logged in")
        return redirect('/')