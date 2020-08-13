from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_server.config import Config


db = SQLAlchemy()


bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
# function name of our route that it reroutes to if not logged in for login required routes (like account page)
login_manager.login_message_category = 'info'
# makes the flashed message have the characteristics of the bootstrap info category


def create_app(config_class=Config):
    # by default when creating an app use the Config class attributes
    app = Flask(__name__)
    app.config.from_object(Config)
    # here we set the config of the app to the same as the object form the config file (with it's properties)

    db.init_app(app)
    # here we use the app created in this function to 'fuel' the extensions created outside the function
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flask_server.routes import main

    app.register_blueprint(main)

    # here we register the blueprints so the routes appear in our app

    return app