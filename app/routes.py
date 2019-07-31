from app import app
from flask import render_template, request
from app.models import model, formopener
from app import back, api

@app.route('/')
@app.route('/index')
def index():
    return render_template("quiz.html")
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
        print(labels)
        print(values)
        return render_template("individual.html", values = values, labels = labels, legend = legend)