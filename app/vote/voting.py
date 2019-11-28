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

        # this returns 0 if it doesn't exist and 1 if it does... in python 0 is equivalent
        # to false and 1 is equivalent to true
        alreadyVoted = redis_cli.exists(f"{userName}")
        if alreadyVoted:
            dogVotes = 0
            catVotes = 0
            message = "You've already voted! You aren't allowed to vote again!"
            listOfKeys = redis_cli.keys("*")
            for key in listOfKeys:
                userVote = redis_cli.get(key).decode("utf-8")
                if userVote == "dogs":
                    dogVotes = dogVotes + 1
                if userVote == "cats":
                    catVotes = catVotes + 1

            return render_template("voting.html", message=message, voteForm=voteForm, listOfKeys=listOfKeys,
                                   dogVotes=dogVotes, catVotes=catVotes, alreadyVoted=alreadyVoted, userVote=userVote)
        redis_cli.set(f"{userName}", userChoice)


    return render_template("voting.html", message=message, voteForm=voteForm)

