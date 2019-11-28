from . import main
from flask import Flask, render_template, request, redirect, session, url_for, flash
from app import redis_cli


@main.route("/clear")
def clear():
    session.clear()
    return redirect("/")

@main.route("/people")
def people():
    # use scan
    keys = redis_cli.keys("*:age")
    peopleList = []
    for key in keys:
        age = redis_cli.get(key)
        # must use key.decode() when pulling info from a redis database
        peopleList.append((key.decode("utf-8"), age.decode("utf-8)")))
    return render_template("people.html", peopleList=peopleList)

@main.route("/")
def index():
    return render_template("index.html", session=session)

