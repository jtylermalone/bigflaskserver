from flask import render_template, session
from app import redis_cli
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired
from . import vote

# this class defines the form that is displayed on the voting.html page.
# it provides a field for the user to enter their name, as well as
# a field of several radio buttons comprised of all the user's options
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

    # default message when user first goes to voting page. This is one of three
    # possible messages that the user may encounter.
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

    # the below if statement executes if the user submits a valid form
    if voteForm.validate_on_submit():
        session["alreadyVoted"] = "yes"
        # get user's animal choice
        userChoice = voteForm.userVote.data
        # get user's name
        userName = voteForm.userName.data

        # here we are querying the database for any key that goes by the same name as that which
        # the user entered. if someone by that name has already voted, the user is taken to the results
        # page, their vote isn't counted, and a relevant message is displayed.

        # redis_cli.exists() returns true or false depending on whether the queried key is found
        # in the database
        alreadyInDatabase = redis_cli.exists(f"{userName}")
        if not alreadyInDatabase:
            # put the user's vote into the database
            redis_cli.set(f"{userName}", userChoice)
            message = "Thank you for voting! Here are the results so far:"
        else: # if the user's entered name is already in the database
            message = "Hey!! You've already voted! You aren't allowed to vote again!"

        # redis_cli.keys("*") returns every single key in the database as a list. below, we are
        # interating through the list and getting each user's vote. depending on the animal
        # found in each vote, the relevant variable is incremented. Each animal's votes are
        # kept track of with their own variable that keeps track of the number of votes for
        # that animal. each of these variables is passed to the voting.html page.
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

    # this return statement executes when the user visits the page for the first time. In this case,
    # the user only sees the voting form.
    return render_template("voting.html", message=message, voteForm=voteForm)

