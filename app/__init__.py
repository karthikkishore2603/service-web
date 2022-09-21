from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
run_with_ngrok(app)

SQLALCHEMY_DATABASE_URL = "mysql://karthik:password@localhost:3306/service"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

db = SQLAlchemy(app)


from . import views, models, crud
