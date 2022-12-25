from .. import app, crud,util
from flask import Flask, request, render_template

from . import admin
from . import technician
@app.get("/")
def login():
    return render_template("login.html")

@app.post("/")
def login_verify():
    username=request.form.get("username")
    password=request.form.get("password")
    role=request.form.get("role")
    if not util.is_valid_password(username,password,role):
        return render_template("check.html")
    if role=="admin":
        return render_template("admin_dashboard.html")
    else:
        return render_template("tech_dashboard.html"),username
