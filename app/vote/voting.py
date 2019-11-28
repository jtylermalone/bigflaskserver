from flask import render_template, session
from app import redis_cli
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, NumberRange
from . import vote

class VoteForm(FlaskForm):
    userName = StringField("Enter your name", validators=[DataRequired()])
    userVote = RadioField("Here are your voting options", choices=[('cats', 'cats'),
                                                                   ('dogs', 'dogs'),
                                                                   ('fish', 'fish')])
    submit = SubmitField("Cast your vote!")

@vote.route("/voting", methods=['POST', 'GET'])
def vote():
    message = "Please register your vote below!"
    voteForm = VoteForm()
    dogVotes = 0
    catVotes = 0
    fishVotes = 0
    if voteForm.validate_on_submit():
        userName = voteForm.userName.data
        alreadyVoted = redis_cli.exists(f"{userName}")
        userChoice = voteForm.userVote.data
        session['userChoice'] = userChoice
        listOfKeys = redis_cli.keys("*")
        for key in listOfKeys:
            userVote = redis_cli.get(key).decode("utf-8")
            if userVote == "dogs":
                dogVotes = dogVotes + 1
            if userVote == "cats":
                catVotes = catVotes + 1
            if userVote == "fish":
                fishVotes = fishVotes + 1
        if not alreadyVoted:
            redis_cli.set(f"{userName}", userChoice)
            message = "Thank you for voting! Here are the results so far:"
        else:
            message = "Hey!! You've already voted! You aren't allowed to vote again!"

        return render_template("voting.html", message=message, voteForm=voteForm,
                               dogVotes=dogVotes, catVotes=catVotes, fishVotes=fishVotes, alreadyVoted=alreadyVoted)



    return render_template("voting.html", message=message, voteForm=voteForm)

