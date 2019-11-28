from flask import render_template, session
from app import redis_cli
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired
from . import vote


class VoteForm(FlaskForm):
    userName = StringField("Enter your name", validators=[DataRequired()])
    userVote = RadioField("Here are your voting options", choices=[('cats', 'cats'),
                                                                   ('dogs', 'dogs'),
                                                                   ('fish', 'fish'),
                                                                   ('birds', 'birds'),
                                                                   ('turtles', 'turtles'),
                                                                   ('goats', 'goats')
                                                                   ])
    submit = SubmitField("Cast your vote!")


@vote.route("/voting", methods=['POST', 'GET'])
def vote():

    # default message when user first goes to voting page
    message = "Please vote below! You may only cast ONE (1) vote!"

    # instantiates VoteForm
    voteForm = VoteForm()

    # must initialize vote count for each choice to 0
    dogVotes = 0
    catVotes = 0
    fishVotes = 0
    birdVotes = 0
    turtleVotes = 0
    goatVotes = 0
    session["alreadyVoted"] = "no"
    if voteForm.validate_on_submit():
        session["alreadyVoted"] = "yes"
        userChoice = voteForm.userVote.data
        userName = voteForm.userName.data
        alreadyInDatabase = redis_cli.exists(f"{userName}")
        if not alreadyInDatabase:
            redis_cli.set(f"{userName}", userChoice)
            message = "Thank you for voting! Here are the results so far:"
        else:
            message = "Hey!! You've already voted! You aren't allowed to vote again!"
        listOfKeys = redis_cli.keys("*")
        for key in listOfKeys:
            userVote = redis_cli.get(key).decode("utf-8")
            if userVote == "dogs":
                dogVotes = dogVotes + 1
            if userVote == "cats":
                catVotes = catVotes + 1
            if userVote == "fish":
                fishVotes = fishVotes + 1
            if userVote == "birds":
                birdVotes = birdVotes + 1
            if userVote == "turtles":
                turtleVotes = turtleVotes + 1
            if userVote == "goats":
                goatVotes = goatVotes + 1
        return render_template("voting.html", message=message, voteForm=voteForm, dogVotes=dogVotes, catVotes=catVotes,
                               fishVotes=fishVotes, birdVotes=birdVotes, turtleVotes=turtleVotes, goatVotes=goatVotes,
                               alreadyInDatabase=alreadyInDatabase)
    return render_template("voting.html", message=message, voteForm=voteForm)

