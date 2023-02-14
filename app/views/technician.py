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
        tasks=crud.get_onsitetasks_by_tech(username=technician.username), technicians=crud.get_all_technicians(),
    )


@app.get("/tech/onsite/viewtask/<task_id>")
def tech_onsite_task_view(task_id):
    print((crud.get_resources_by_id(task_id)))
    return render_template(
        "tech_onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id), technicians=crud.get_all_technicians(),
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
    return render_template("tech_customer.html", customers=crud.get_all_customer())


@app.post("/tech/customers")
def tech_customers_filter():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "tech_customer.html",
            customers=crud.get_all_customer(filter=data)
            
        )
    return redirect(url_for("customers"))
@app.get("/tech/customers/work/<customer_id>")
def tech_customer_works(customer_id):
    return render_template(
        "tech_customers_works.html",
        tasks=crud.get_task_by_cust_id(customer_id),
    )


@app.get("/tech/instore")
def tech_instore():
    technician = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not technician:
        return render_template("check.html")
    return render_template("tech_instore.html",tasks=crud.get_instoretasks_by_tech(username=technician.username))

@app.get("/tech/instore/add")
def tech_instore_add_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "tech_instore_add_task.html", technicians=crud.get_all_technicians(), flag=False
    )

@app.get("/tech/instore/task/<in_task_id>")
def tech_instore_task_view_by_id(in_task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "tech_instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(in_task_id),
        technicians=crud.get_all_technicians(),
    )