from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


SQLALCHEMY_DATABASE_URL = "mysql://karthik:password@localhost:3306/service"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config[
    "SECRET_KEY"
] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"

db = SQLAlchemy(app)


from . import views, models, crud
