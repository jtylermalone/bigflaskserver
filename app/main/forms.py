from . import main
from app import redis_cli
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class SampleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[NumberRange(13, 120)])
    submit = SubmitField('Submit!')

@main.route("/form", methods=['POST', 'GET'])
def form():
    name = None
    age = None
    sampleForm = SampleForm()
    if sampleForm.validate_on_submit():
        name = sampleForm.name.data
        age = sampleForm.age.data
        session['name'] = name
        session['age'] = age
        redis_cli.set(f"{name}:age", age)
        redis_cli.set(f"{name}:name", name)
        return redirect("/")
    return render_template('form.html', sampleForm=sampleForm)