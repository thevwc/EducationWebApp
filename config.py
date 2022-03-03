# config.py # AzureMonitorScheduling

import os
#import pyodbc
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

# LOAD dotenv IN THE BASE DIRECTORY
basedir = os.path.abspath(os.path.dirname(__file__))


envFileName = ".env"
if not Path(envFileName).exists():
   print(f"Cant load a file named {envFileName} from the current dir") #TBD dump to stderr
   exit(-1)
print(f"Loading env vars from a file named {envFileName}")
load_dotenv(os.path.join(basedir, envFileName))

driver     = os.getenv('Driver',     "No Driver env var found")
server     = os.getenv('Server',     "No server env var found")
database   = os.getenv('Database',   "No Database env var found")
dbUserName = os.getenv('DBUsername', "No DBUserName env var found")
dbPassword = os.getenv('DBPassword', "No DBPassword env var found")

params = urllib.parse.quote_plus('DRIVER='   + driver     + ';'
                                 'SERVER='   + server     + ';'
                                 'DATABASE=' + database   + ';'
                                 'UID='      + dbUserName + ';'
                                 'PWD='      + dbPassword + ';')
conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

class Config(object):
    SECRET_KEY = os.environ.get('Secret_key') or 'juniorbr549wells'
    SQLALCHEMY_DATABASE_URI = conn_str 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD=True 
        
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = False
    ADMINS = ['hartl1r@gmail.com']
    ACCOUNT_ID = os.environ.get('account_id')
    REFRESH_TOKEN = os.environ.get('refresh_token')
    CLIENT_SECRET = os.environ.get('client_secret')
    CLIENT_ID = os.environ.get('client_id')
