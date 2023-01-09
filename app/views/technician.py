from flask import render_template, request, redirect, url_for, session

from .. import app, crud, util, models


@app.get("/tech/dashboard")
def tech_dashboard():
    return render_template("tech_dashboard.html")


@app.get("/tech/onsite")
def tech_onsite():
    technician = crud.get_technician(username=session["username"])
    return render_template(
        "tech_onsite.html",
        customers=crud.get_all_customer(),
        tasks=crud.get_onsitetasks_by_tech(username=session["username"]),
    )


@app.get("/tech/customer")
def tech_customer():
    return render_template("tech_customer.html")


@app.get("/tech/instore")
def tech_instore():
    return render_template("tech_instore.html")
