from .. import app,crud,util
from flask import request, render_template

@app.get("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.get("/admin/technician")
def add_technician():
    return render_template("add_technician.html")