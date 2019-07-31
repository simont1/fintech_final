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
    
@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "GET":
        return "Nothing to see here! Go back."
    else:
        user_data = request.form
        investment_amount = float(user_data["investment_amount"])
        # print(investment_amount)
        display = back.price_range(investment_amount)
        # print(display)
        volatility = user_data['volatility']
    return render_template("results.html", stocks = display)
    
    
@app.route('/individual', methods=["GET", "POST"])
def individual():
    if request.method == "GET":
        return "Nothing to see here! Go back."
    else:
        user_data = request.form
        labels = api.labels(user_data['symbol'])
        legend = "Daily data for the past year"
        values = api.values(user_data['symbol'])
        # print(labels)
        # print(values)
        return render_template("individual.html", values = values, labels = labels, legend = legend, symbol = user_data['symbol'])