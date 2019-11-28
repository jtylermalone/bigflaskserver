from flask import render_template, session
import random
from . import guessinggame
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
# random.randint(5)

targetNum = random.randint(1, 100)

class GuessForm(FlaskForm):
    numberGuess = IntegerField("Guess", validators=[NumberRange(0, 100), DataRequired("Number required")])
    submit = SubmitField("Make Guess")


@guessinggame.route("/guessinggame", methods=['POST', 'GET'])
def game():
    if not session.get("my_number"):
        ## Debug Printout
        print("My number hsan't been generated yet.. generating now.")
        session["my_number"] = random.randint(1, 100)
    else:
        ## DEbug printout
        print(f"My number is set: { session.get('my_number') }")
    message = "I am thinking of a number between 0 and 100."
    guessForm = GuessForm()
    if guessForm.validate_on_submit():
        numberGuess = guessForm.numberGuess.data
        if numberGuess < session.get("my_number"):
            message = "Your guess is too low."
        elif numberGuess > session.get("my_number"):
            message = "Your guess is too high."
        elif numberGuess == session.get("my_number"):
            message = f"You guessed correctly! I was thinking of { session.get('my_number') }. Play again!"
            session['my_number'] = random.randint(1, 100)

    return render_template("game.html", message=message, guessForm=guessForm)
