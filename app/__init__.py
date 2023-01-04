from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


SQLALCHEMY_DATABASE_URL = "mysql://karthik:password@localhost:3306/service"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

db = SQLAlchemy(app)


from . import views, models, crud
