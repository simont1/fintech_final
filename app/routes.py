from app import app
from flask import render_template, request
from app.models import model, formopener
from app import back

@app.route('/')
@app.route('/index')
def index():
    return render_template("quiz.html")
@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "GET":
        return "Your stocks are ready"
    else:
        user_data = request.form
        investment_amount = float(user_data["investment_amount"])
        print(investment_amount)
        display = back.price_range(investment_amount)
        # print(display)
        print(int(500/477.45))
    return render_template("results.html", stocks = display)