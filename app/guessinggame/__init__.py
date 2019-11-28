from flask import Blueprint

guessinggame = Blueprint("guessinggame", __name__, template_folder='templates')

from . import game