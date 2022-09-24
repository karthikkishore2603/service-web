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

@app.get("/admin/chiplevel")
def chiplevel():
    return render_template("chiplevel.html")

@app.get("/admin/warranty")
def warranty():
    return render_template("warranty.html")

@app.get("/admin/expenditure")
def expenditure():
    return render_template("expenditure.html")

@app.get("/admin/order")
def order():
    return render_template("order.html")

@app.get("/admin/followup")
def follow_up():    
    return render_template("follow_up.html")