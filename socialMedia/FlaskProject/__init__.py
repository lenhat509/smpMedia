import os
from flask import Flask, Blueprint
#from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from FlaskProject.config import Config



mail = Mail()
#mysql= MySQL()
bcrypt= Bcrypt()
db= SQLAlchemy()
login_manager= LoginManager()
login_manager.login_view ='users.login'


def create_app(default_config=Config):
    app = Flask(__name__) 
    app.config.from_object(Config)
    mail.init_app(app)
    #mysql.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    from FlaskProject.main.routes import main
    from FlaskProject.users.routes import users
    from FlaskProject.posts.routes import posts
    from FlaskProject.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app


