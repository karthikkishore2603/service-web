from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from . import constants
import pymysql
from fpdf import FPDF

pymysql.install_as_MySQLdb()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLALCHEMY_DATABASE_URL
app.config["SECRET_KEY"] = constants.FLASK_SECRET_KEY
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
db = SQLAlchemy(app, create_engine(constants.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True))
"""
engine = create_engine(constants.SQLALCHEMY_DATABASE_URL, 
                       connect_args={'charset': 'utf8mb4', 'autocommit': True})
connection = engine.connect()
db=SQLAlchemy(app, engine)
"""


from . import views, models, crud, pdf
