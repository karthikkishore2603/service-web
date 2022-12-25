from flask import render_template, request, redirect, url_for

from .. import app, crud, util, models

@app.get("/tech/dashboard")
def tech_dashboard():
    return render_template("tech_dashboard.html")

@app.get("/tech/onsite")
def tech_onsite():
    return render_template("tech_onsite.html",customers=crud.get_all_customer(), tasks=crud.get_onsitetasks_by_tech(), technicians=crud.get_all_technicians())

@app.get("/tech/customer")
def tech_customer():
    return render_template("tech_customer.html")


@app.get("/tech/instore")
def tech_instore():
    return render_template("tech_instore.html")
