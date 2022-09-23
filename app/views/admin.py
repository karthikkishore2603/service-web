from .. import app,crud,util
from flask import request, render_template

@app.get("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.get("/admin/technician")
def technician():
    return render_template("technician.html")

@app.get("/admin/onsite")
def onsite():
    return render_template("onsite.html")

@app.get("/admin/instore")
def instore():
    return render_template("instore.html")