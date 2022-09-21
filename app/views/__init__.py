from .. import app, crud
from flask import Flask, request, render_template

@app.get("/")
def login():
    return "hello"