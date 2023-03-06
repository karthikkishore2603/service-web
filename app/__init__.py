from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import constants
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLALCHEMY_DATABASE_URL
app.config["SECRET_KEY"] = constants.FLASK_SECRET_KEY

db = SQLAlchemy(app)


from . import views, models, crud, pdf
