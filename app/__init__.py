from flask_bootstrap import Bootstrap
from flask import Flask
from config import config
from flask_redis import FlaskRedis

# here, you initialize all modules that you need for your application

# instantiate modules:
bootstrap = Bootstrap()
redis_cli = FlaskRedis()

def create_app(config_name):
    # instantiating the application itself
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize boostrap module:
    bootstrap.init_app(app)
    redis_cli.init_app(app)

    # registering blueprints in the app:
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from .guessinggame import guessinggame as guessinggame_blueprint
    app.register_blueprint(guessinggame_blueprint)

    from .vote import vote as vote_blueprint
    app.register_blueprint(vote_blueprint)

    return app
