from flask import render_template, request, redirect, url_for

from .. import app, crud, util, models


@app.get("/tech/dashboard")
def tech_dashboard():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_dashboard.html")


@app.get("/tech/onsite")
def tech_onsite():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template(
        "tech_onsite.html",
        customers=crud.get_all_customer(),
        tasks=crud.get_onsitetasks_by_tech(username=technician.username),
    )

@app.get("/tech/onsite/viewtask/<task_id>")
def tech_onsite_task_view(task_id):
    print((crud.get_resources_by_id(task_id)))
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
    )

@app.post("/tech/onsite/viewtask/<task_id>")
def tech_onsite_task_update(task_id):
    data = dict(request.form)
    data["task_id"] = task_id
    crud.update_onsitetasks(data)
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
    )

@app.get("/tech/customer")
def tech_customer():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_customer.html")

@app.get("/tech/customers/work/<customer_id>")
def tech_customer_works(customer_id):
    return render_template(
        "tech_customers_works.html",tasks=crud.get_onsitetask_by_cust_id(customer_id),
    )

@app.get("/tech/instore")
def tech_instore():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_instore.html")
