from .. import app
from flask import Flask, render_template

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")