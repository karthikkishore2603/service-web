from .. import app,crud,util
from flask import request, render_template

@app.get("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.get("/admin/technician")
def technician():
    return render_template("technician.html",technicians=crud.get_all_technicians(),admins=crud.get_all_admins())


@app.post("/admin/technician")
def technician_post():
    data=dict(request.form)
    type = data.pop("role")
    crud.create_user(data,type)
    return render_template("technicians.html")



@app.get("/admin/customers")
def customers():
    return render_template("customers.html")

@app.get("/admin/onsite")
def onsite():
    return render_template("onsite.html")

@app.post("/admin/onsite/")
def onsite_add_task():
    data=dict(request.form)
    crud.create_task(data)
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

