from flask import render_template, session
from app import redis_cli
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, NumberRange
from . import vote

class VoteForm(FlaskForm):
    userName = StringField("Enter your name")
    userVote = RadioField("Here are your voting options", choices=[('cats', 'cats'),
                                      ('dogs', 'dogs')])
    submit = SubmitField("Cast your vote!")

@vote.route("/voting", methods=['POST', 'GET'])
def vote():
    message = "Please register your vote below!"
    voteForm = VoteForm()
    if voteForm.validate_on_submit():
        userName = voteForm.userName.data
        userChoice = voteForm.userVote.data
        session['userChoice'] = userChoice
        alreadyVoted = redis_cli.exists(f"{userName}:vote")
        if alreadyVoted:
            message = "You've already voted! You aren't allowed to vote again!"
            return render_template("voting.html", message=message)
        redis_cli.set(f"{userName}:vote", userChoice)


    return render_template("voting.html", message=message, voteForm=voteForm)

