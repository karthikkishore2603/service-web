from flask import render_template, request, redirect, url_for, make_response

from .. import app, crud, util, models, pdf


@app.get("/admin/dashboard")
def admin_dashboard():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("admin_dashboard.html")


@app.get("/admin/technician")
def technician():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "technician.html",
        technicians=crud.get_all_technicians(),
        admins=crud.get_all_admins(),
    )


@app.post("/admin/technician")
def technician_post():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    data = dict(request.form)

    try:
        crud.create_technician(data)
    except Exception as e:
        return render_template(
            "technician.html",
            technicians=crud.get_all_technicians(),
            admins=crud.get_all_admins(),
            errors=str(e).split(","),
        )

    return redirect(url_for("technician"))


@app.get("/admin/technician/work/<technician_id>")
def technician_task_view(technician_id):
    return render_template(
        "technician_task_view.html",
        tasks=crud.get_onsitetask_by_tech_id(technician_id),
    )


@app.post("/admin/technician")
def technician_filter():
    if request.form.get("ftechnician"):
        return render_template(
            "technician.html",
            technicians=crud.get_technicians(username=request.form.get("ftechnician")),
        )
    else:
        return redirect(url_for("technician"))

@app.get("/admin/partners")
def partners():
    return render_template("partners.html", partners=crud.get_all_partners())

@app.post("/admin/partners")
def partners_add():
    data = dict(request.form)
    try:
        crud.create_partners(data)
    except Exception as e:
        return render_template(
            "partners.html",
            partners=crud.get_all_partners()
        )
    return redirect(url_for("partners"))

@app.get("/admin/customers")
def customers():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("customers.html", customers=crud.get_all_customer())


@app.get("/admin/customers/work/<customer_id>")
def customer_works(customer_id):
    return render_template(
        "customer_works.html",
        tasks=crud.get_onsitetask_by_cust_id(customer_id),
    )


@app.get("/admin/customers/work/<customer_id>")
def customer_work_download(customer_id):
    pdf_data = make_response(
        pdf.create_customer_work_pdf(
            tasks=crud.get_onsitetask_by_cust_id(customer_id=customer_id)
        )
    )
    pdf_data.headers["Content-Disposition"] = "attachment;"
    pdf_data.headers["Content-Type"] = "application/pdf"
    return pdf_data


@app.get("/admin/onsite")
def onsite():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "onsite.html",
        customers=crud.get_all_customer(),
        tasks=crud.get_all_onsitetasks(),
        technicians=crud.get_all_technicians(),
    )


@app.post("/admin/onsite")
def onsite_add_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "onsite.html",
            tasks=crud.get_all_onsitetasks(filter=data),
            technicians=crud.get_all_technicians(),
        )
    try:
        crud.create_task(data)
    except Exception as e:
        return render_template(
            "onsite.html",
            tasks=crud.get_all_onsitetasks(),
            technicians=crud.get_all_technicians(),
            errors=str(e).split(","),
        )
    return redirect(url_for("onsite"))


@app.get("/admin/onsite/<task_id>/update_status")
def admin_onsite_update_status(task_id):
    resource = crud.get_resources_by_id(task_id=task_id)
    message=""
    if not resource:
        message="Update resource first"
    elif resource.received_charge < resource.service_charge:
        message="Service charge is not received"
    else:
        flag = crud.update_onsite_task_status(task_id)
        if flag:
            message="Status updated"
        else:
            message="Already closed"
    return render_template(
        "onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=message,
    )


@app.get("/admin/onsite/viewtask/<task_id>")
def onsite_task_view(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    print((crud.get_resources_by_id(task_id)))
    return render_template(
        "onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=None,
    )


@app.post("/admin/onsite/viewtask/<task_id>")
def onsite_task_update(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    resource = crud.get_resources_by_id(task_id=task_id)
    message = ""
    if resource and resource.status == "Completed":
        message="Task is already completed"
    else:
        data = dict(request.form)
        data["task_id"] = task_id
        crud.update_onsitetasks(data)
        message="Successfully updated"
    return render_template(
        "onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=message,
    )


@app.get("/admin/onsite/download/<task_id>")
def onsite_task_download(task_id):
    pdf_data = make_response(
        pdf.create_pdf(
            tasks=crud.get_onsitetask_by_id(task_id=task_id),
            resources=crud.get_resources_by_id(task_id),
        )
    )
    pdf_data.headers["Content-Disposition"] = "attachment;"
    pdf_data.headers["Content-Type"] = "application/pdf"
    return pdf_data


@app.get("/admin/instore")
def instore():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("instore.html", tasks=crud.get_all_instoretasks())


@app.get("/admin/instore/add")
def instore_add_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "instore_add_task.html", technicians=crud.get_all_technicians(), flag=False
    )


@app.get("/admin/instore/task/<in_task_id>")
def instore_task_view_by_id(in_task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template(
        "instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(in_task_id),
        technicians=crud.get_all_technicians(),
    )


@app.post("/admin/instore/add")
def instore_add_task_view():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    data = dict(request.form)
    crud.create_instore_task(data)

    return render_template(
        "instore_add_task.html",
        technicians=crud.get_all_technicians(),
        tasks={},
        flag=False,
    )


@app.post("/admin/instore/task/<in_task_id>")
def instore_task_update(in_task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    data = dict(request.form)
    data["in_task_id"] = in_task_id
    crud.update_instoretasks(data)
    return render_template(
        "instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(in_task_id),
        technicians=crud.get_all_technicians(),
    )


@app.get("/admin/chiplevel")
def chiplevel():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("chiplevel.html")


@app.get("/admin/chiplevel/task/<in_task_id>")
def chiplevel_add(in_task_id):
    data = dict(request.form)
    print(data)
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("chiplevel_add_task.html", tasks=crud.get_instoretask_by_id(in_task_id),partners=crud.get_all_partners())

@app.post("/admin/chiplevel/task/<in_task_id>")
def chiplevel_update_task(in_task_id):
    data = dict(request.form)
    print(data)
    crud.chiplevel_update_task(data)
    return render_template("chiplevel_add_task.html", tasks=crud.get_instoretask_by_id(in_task_id),partners=crud.get_all_partners())


@app.get("/admin/warranty")
def warranty():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("warranty.html")


@app.get("/admin/warranty/task/<in_task_id>")
def warranty_add(in_task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("warranty_add_task.html", tasks=crud.get_instoretask_by_id(in_task_id),partners=crud.get_all_partners())

@app.post("/admin/warranty/task/<in_task_id>")
def warranty_update_task(in_task_id):
    data = dict(request.form)
    print(data)
    crud.warranty_update_task(data)
    return render_template("chiplevel_add_task.html", tasks=crud.get_instoretask_by_id(in_task_id),partners=crud.get_all_partners())

@app.get("/admin/expenditure")
def expenditure():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("expenditure.html")


@app.get("/admin/order")
def order():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("order.html")


@app.get("/admin/followup")
def follow_up():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("follow_up.html")


@app.get("/admin/quotation")
def quotation():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    return render_template("quotation.html", quotation=crud.get_all_quotation())


@app.post("/admin/quotation")
def quotation_create():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request) or not admin:
        return render_template("check.html")
    data = dict(request.form)
    try:
        crud.create_quotation(data)
    except Exception as e:
        return render_template(
            "quotation.html",
            quotation=crud.get_all_quotation(),
            errors=str(e).split(","),
        )

    return render_template("quotation.html", quotation=crud.get_all_quotation())
