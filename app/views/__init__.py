from asyncio.windows_events import NULL
from pickle import NONE
from .. import app, crud,util
from flask import Flask, request, render_template

@app.get("/")
def login():
    return render_template("login.html")

@app.post("/")
def login_verify():
    username=request.form.get("username")
    password=request.form.get("password")
    if util.is_valid_password(username,password):
        return render_template("check.html")
    else:
        return "wrong"
