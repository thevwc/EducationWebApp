# __init__.py

import logging

# from logging.handlers import RotatingFileHandler
# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_mail import Mail, Message

logger = None


def InitLogging():
    """
    Inits the logging subsystem
    """
    LOG_FILE = "education.log"

    global logger
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    formatString = "%(asctime)s %(module)-4s %(levelname)-7s %(message)s"
    LoggerFileHandler = logging.FileHandler(LOG_FILE, 'a')
    LoggerFileHandler.setFormatter(logging.Formatter(formatString, "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(LoggerFileHandler)


InitLogging()
logger.debug("Started Education web app")

app = Flask(__name__)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True

mail = Mail(app)

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

from app import routes, models, errors
