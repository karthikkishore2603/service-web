from flask import render_template, request, redirect, url_for

from .. import app, crud, util


@app.get("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.get("/admin/technician")
def technician():
    return render_template(
        "technician.html",
        technicians=crud.get_all_technicians(),
        admins=crud.get_all_admins(),
    )


@app.post("/admin/technician")
def technician_post():
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

    return render_template(
        "technician.html",
        technicians=crud.get_all_technicians(),
        admins=crud.get_all_admins(),
    )


@app.get("/admin/customers")
def customers():
    return render_template("customers.html", customers=crud.get_all_customer())


@app.get("/admin/onsite")
def onsite():
    return render_template("onsite.html",customers=crud.get_all_customer(), tasks=crud.get_all_onsitetasks(), technicians=crud.get_all_technicians(),)


@app.post("/admin/onsite")
def onsite_add_task():
    data = dict(request.form)
    if(data.get("ftype")):
        return render_template("onsite.html", tasks=crud.get_all_onsitetasks(filter=data) ,technicians=crud.get_all_technicians())
    crud.create_task(data)
    return render_template("onsite.html", tasks=crud.get_all_onsitetasks() ,technicians=crud.get_all_technicians())

@app.get("/admin/onsite/viewtask/<task_id>")
def onsite_task_view(task_id):
    print((crud.get_resources_by_id(task_id)))
    return render_template("onsite_task_view.html",tasks=crud.get_onsitetask_by_id(task_id), resources=crud.get_resources_by_id(task_id))

@app.post("/admin/onsite/viewtask/<task_id>")
def onsite_task_update(task_id):
    data = dict(request.form)
    data['task_id']=task_id
    crud.update_onsitetasks(data)
    return render_template("onsite_task_view.html",tasks=crud.get_onsitetask_by_id(task_id),resources=crud.get_resources_by_id(task_id))

@app.get("/admin/instore")
def instore():
    return render_template("instore.html")

@app.get("/admin/instore/add")
def instore_add_task():
    return render_template("instore_add_task.html")

@app.post("/admin/instore/add")
def instore_update_task():
    data = dict(request.form)
    
    print(data)
    return render_template("instore_add_task.html")

@app.post("/admin/instore/add/items")
def instore_update_task_items():
    data = dict(request.form)
    print(data)
    return render_template("instore_add_task.html")

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
