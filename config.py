import os
basedir = os.path.abspath(os.path.dirname(__file__))

# export FLASK_APP=bigflaskserver.py


class Config:
    SECRET_KEY = "csci315"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}