# __init__.py

#import logging
#from logging.handlers import RotatingFileHandler
#import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from app import routes, models, errors