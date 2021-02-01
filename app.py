from flask import Flask, render_template, request, redirect, url_for
from flask.globals import request
from werkzeug.utils import redirect
app = Flask(__name__)


@app.route("/", methods = ["POST", "GET"])
def after_input():
    if request.method == "POST":
        list_of_dices = [request.form.get('roll1'), request.form.get('roll2'), request.form.get('roll3')] 
        throws = request.form.get("throw")        
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

        return render_template("index.html", three_of_a_kind = f"{list_of_probs[0]}%", four_of_a_kind = f"{list_of_probs[1]}%", 
        full_house_prob = f"{list_of_probs[2]}%", yahtzee_prob = f"{list_of_probs[3]}%", old_1 = die1, old_2 = die2, old_3 = die3, 
        max_prob = max_prob, old_throw = "1")
    else:
        return render_template("index.html", old_1 = "1", old_2 = "1", old_3 = "1", old_throw = "2")

def calc_prob(die1, die2, die3, throwcount):
    if throwcount == "1":
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
