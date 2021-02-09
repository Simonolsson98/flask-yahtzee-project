from flask import Flask, render_template, request, redirect, url_for
from flask.globals import request
from werkzeug.utils import redirect
import numpy as np

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("base.html")


@app.route("/yahtzee", methods = ["POST", "GET"])
def after_input():
    if request.method == "POST" or request.method == "GET":
        roll1 = 1
        roll2 = 1
        roll3 = 1
        try:
            list_of_dices = [int(request.form.get('roll1')), int(request.form.get('roll2')), int(request.form.get('roll3'))] 
            throws = int(request.form.get("throw"))
        except:
            roll1 = np.random.randint(1, 7)
            roll2 = np.random.randint(1, 7)
            roll3 = np.random.randint(1, 7)
            list_of_dices = [1, 1, 1]
            throws = 2

        die1 = list_of_dices[0]
        die2 = list_of_dices[1]
        die3 = list_of_dices[2]
        list_of_probs = calc_prob(die1, die2, die3, throws)
        if max(list_of_probs) == 100: #ignore 100% since you cant "go for" something you already have
            max_probability = sorted(list_of_probs, reverse=True)[1]
        else:
            max_probability = max(list_of_probs)
        index = list_of_probs.index(max_probability)
        if index == 0:
            max_prob = "three of a kind"
        elif index == 1:
            max_prob = "four of a kind"
        elif index == 2:
            max_prob = "full house"
        else: 
            max_prob = "yahthee"
        if list_of_dices.count(1) == 3:
            ones = 100
        else:
            ones = 100 * round((5 - list_of_dices.count(1)) * (1 / 6), 3) #TODO: figure out math here
        if list_of_dices.count(2) == 3:
            twos = 100
        else:
            twos = 100 * round((5 - list_of_dices.count(2)) * (1 / 6), 3) #TODO: figure out math here
        if list_of_dices.count(3) == 3:
            threes = 100
        else: 
            threes = 100 * round((5 - list_of_dices.count(3)) * (1 / 6), 3) #TODO: figure out math here

        return render_template("index.html", three_of_a_kind = f"{list_of_probs[0]}%", four_of_a_kind = f"{list_of_probs[1]}%", 
        full_house_prob = f"{list_of_probs[2]}%", yahtzee_prob = f"{list_of_probs[3]}%", old_1 = die1, old_2 = die2, old_3 = die3, 
        max_prob = max_prob, old_throw = 1, ones = f"{ones}%", twos = f"{twos}%", threes = f"{threes}%", roll1 = roll1, roll2 = roll2, 
        roll3 = roll3)
    else:
        return render_template("index.html", old_1 = 1, old_2 = 1, old_3 = 1, old_throw = 2, roll1 = 1, roll2 = 2, roll3 = 3)    

def calc_prob(die1, die2, die3, throwcount):
    if throwcount == 1:
        if(die1 == die2 and die2 == die3):
            return [1 * 100, round(2/6 * 100, 2), round(1/6 * 100, 2), round(1/(6**2) * 100, 2)]
        elif(die1 == die2 or die2 == die3 or die1 == die3):
            return [round(3/6 * 100, 2), round((347/4997) * 100, 2), round(0.2222 * 100, 2), round(1/(6**3) * 100, 4)]
        return ["error","error","error","error"]
    else: #throwcount = 2
        if(die1 == die2 and die2 == die3):
            return [1 * 100, round(4/6 * 100, 2), round(2/6 * 100, 2), round(2/(6**2) * 100, 2)]
        elif(die1 == die2 or die2 == die3 or die1 == die3):
            return [round((132/216) * 100, 2), round(0.11574*2 * 100, 2), round(0.4444 * 100, 2), round(2/(6**3) * 100, 4)]
        return ["error","error","error","error"]


if __name__ == "__main__":
    app.run(debug=True)
