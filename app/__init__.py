from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import flask_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
app.secret_key = '5hJ2kR9sL7pT3wFq'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from app import views
from app import auth_views
from app import admin_views
from app import user_views
from app import class_views
from app import trainer_views
from app import error_handler