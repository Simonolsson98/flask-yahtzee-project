from flask import Flask, render_template, request, redirect, url_for
from flask.globals import request
from werkzeug.utils import redirect
app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html", old_1 = 1, old_2 = 1, old_3 = 1)

@app.route("/hello", methods = ["POST", "GET"])
def after_input():
    if request.method == "POST":
        list_of_dices = [request.form.get('roll1'), request.form.get('roll2'), request.form.get('roll3')] 
        throws = request.form.get("throw")        
        die1 = list_of_dices[0]
        die2 = list_of_dices[1]
        die3 = list_of_dices[2]
        list_of_probs = calc_prob(die1, die2, die3, throws)

        return render_template("index.html", tretal_prob = f"{list_of_probs[0]*100}%", fyrtal_prob = f"{list_of_probs[1]*100}%", 
        full_house_prob = f"{list_of_probs[2]*100}%", yahtzee_prob = f"{list_of_probs[3]*100}%", old_1 = die1, old_2 = die2, old_3 = die3)
    else:
        return redirect("/")

def calc_prob(die1, die2, die3, throwcount):
    if throwcount == "1":
        if(die1 == die2 and die2 == die3):
            return [1, round(2/6, 2), round(1/6, 2), round(1/(6**2), 2)]
        elif(die1 == die2 or die2 == die3 or die1 == die3):
            return [round(3/6, 2), round(347/4997, 2), round(0.2222, 2), round(1/(6**3), 2)]
            pass
        return [-1,-1,-1,-1]
    else: #throwcount = 2
        if(die1 == die2 and die2 == die3):
            return [1, round(4/6, 2), round(2/6, 2), round(2/(6**2), 2)]
        elif(die1 == die2 or die2 == die3 or die1 == die3):
            pass
        return [-1,-1,-1,-1]


if __name__ == "__main__":
    app.run(debug=True)
