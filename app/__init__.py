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

e= create_engine(constants.SQLALCHEMY_DATABASE_URL, echo=True)
c = e.connect()
db = SQLAlchemy(app, create_engine(constants.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True))




from . import views, models, crud, pdf
