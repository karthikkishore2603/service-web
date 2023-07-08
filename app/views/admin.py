from flask import render_template, request, redirect, url_for, make_response,json,Response, jsonify
import pymysql
import time 
from datetime import datetime
from .. import app, crud, util, models, pdf
from fpdf import FPDF
import pytz
 
@app.get("/admin/dashboard")
def admin_dashboard():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("admin_dashboard.html", onsite_task_count=crud.get_onsite_count(), instore_task_count_open=crud.get_instore_count_open()
    ,instore_task_count_pending=crud.get_instore_count_pending(), get_chiplevel_count_sent=crud.get_chiplevel_count_sent(),
    get_warranty_count_sent=crud.get_warranty_count_sent(),)


@app.get("/admin/technician")
def technician():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "technician.html",
        technicians=crud.get_all_technicians(),
        admins=crud.get_all_admins(),
    )


@app.post("/admin/technician")
def technician_post():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "technician.html",
            technicians=crud.get_all_technicians(filter=data),
            
        )
    
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
        "work_view.html",
        tasks=crud.get_onsitetask_by_tech_id(technician_id),
    )

@app.get("/admin/technician/work/instore/<technician_id>")
def technician_instore_task_view(technician_id):
    return render_template(
        "instore_work_view.html",
        tasks=crud.get_instore_by_tech_id(technician_id),
    )


@app.get("/admin/partners")
def partners():
    
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    names = crud.get_all_partner_name()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    return render_template("partners.html", partners=crud.get_all_partners(),name=(name_lit),flag=0)

@app.post("/admin/partners")
def partners_add():
    data = dict(request.form)
    names = crud.get_all_partner_name()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])

    
    if data.get("ftype"):
        return render_template(
            "partners.html",
            partners=crud.get_all_partners(filter=data),name=(name_lit),flag=0
        )
    try:
        crud.create_partners(data)
    except Exception as e:
        return render_template(
            "partners.html",
            partners=crud.get_all_partners(),name=(name_lit),
            errors=str(e).split(",")
        )
    return redirect(url_for("partners"))


@app.get("/admin/partners/work/<partner_id>")
def partner_work_view(partner_id):
    return render_template(
        "partner_work_view.html",
        tasks=crud.get_partner_by_id(partner_id),
    )

@app.get("/admin/customers")
def customers():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    names = crud.get_all_customer_name()
    
    phone = crud.get_all_customer_phone()
    name_lit =[]
    phone_lit = []
    for i in names:
        name_lit.append(i[0])

    for i in phone:
        phone_lit.append(i[0])
    
    return render_template("customers.html", customers=crud.get_all_customer(),name=(name_lit),phone=(phone_lit),flag=0)

@app.post("/admin/customers")
def customers_filter():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    names = crud.get_all_customer_name()
    
    phone = crud.get_all_customer_phone()
    name_lit =[]
    phone_lit = []
    for i in names:
        name_lit.append(i[0])

    for i in phone:
        phone_lit.append(i[0])
    
    if data.get("ftype"):
        return render_template(
            "customers.html",
            customers=crud.get_all_customer(filter=data),name=(name_lit),phone=(phone_lit),flag=0
            
        )
    return redirect(url_for("customers"))


@app.get("/admin/customers/work/<customer_id>")
def customer_task_view(customer_id):
    return render_template(
        "work_view.html",tasks=crud.get_task_by_cust_id(customer_id))

  

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
    if not util.is_user_authenticated(request,type="admin") or not admin:
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
    if (not util.is_user_authenticated(request,type="admin") or not admin) :
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
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=None,
    )

@app.get("/admin/viewtask/<task_id>/<t_name>")
def task_view(task_id,t_name):
    admin = util.current_user_info(request)
    print(t_name)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    tasks=crud.task_by_id(task_id)
    if t_name=="ON":
        return redirect(url_for("onsite_task_view",task_id=task_id))
    
    else:
        return redirect(url_for("instore_task_view_by_id",task_id=task_id))
    


@app.post("/admin/onsite/viewtask/<task_id>")
def onsite_task_update(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    resource = crud.get_resources_by_id(task_id=task_id)
    tasks=crud.get_onsitetask_by_id(task_id=task_id)

    message = ""
    if resource and tasks.status == "Completed":
        message="Task is already completed"
    else:
        data = dict(request.form)
        data["task_id"] = task_id
        try:
            crud.update_onsitetasks(data)
            print(data)
            message="Successfully updated"
        except Exception as e:
            return render_template(
                "onsite_task_view.html",
                tasks=crud.get_onsitetask_by_id(task_id),
                resources=crud.get_resources_by_id(task_id),
                message=message,
                errors=str(e).split(","),
        )
    
        
    return render_template(
        "onsite_task_view.html",
        tasks=crud.get_onsitetask_by_id(task_id),
        resources=crud.get_resources_by_id(task_id),
        message=message,
    )

"""
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
"""

@app.get("/admin/instore")
def instore():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    names = crud.get_all_customer_phone()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    return render_template("instore.html", tasks=crud.get_all_instoretasks(),phone=(name_lit))

@app.post("/admin/instore")
def instore_filter_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    
    names = crud.get_all_customer_phone()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    if data.get("ftype"):
        return render_template(
            "instore.html",
            tasks=crud.get_all_instoretasks(filter=data),
            technicians=crud.get_all_technicians(),phone=(name_lit)
            
        )
    crud.create_task(data)

    return redirect(url_for("instore"))
"""
@app.get("/admin/instore/add")
def instore_add_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "instore_add_task.html", technicians=crud.get_all_technicians(),tasks={}, flag=False
    )
"""

@app.get("/admin/instore/task/<task_id>")
def instore_task_view_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(task_id),
        technicians=crud.get_all_technicians(),
    )


@app.route("/admin/instore/add", methods=["POST","get"])
def instore_add_task_view():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    names = crud.get_all_customer_name()
    
    name_lit =[]
    for i in names:
        name_lit.append(i[0])

    phone = crud.get_all_customer_phone()
    
    phone_lit =[]
    for i in phone:
        phone_lit.append(i[0])

    if request.method == "POST":
        print('heloo')
        data =dict(request.form)
        print(data)

        crud.create_instore_task(data)
        return redirect(url_for("instore"))
    else:
        return render_template(
        "instore_add_task.html", technicians=crud.get_all_technicians(),tasks={}, flag=False,name=(name_lit),phone=(phone_lit)
    )


@app.post("/admin/instore/task/<task_id>")
def instore_task_update(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    data = dict(request.form)
    data["task_id"] = task_id
    crud.update_instoretasks(data)
    return render_template(
        "instore_add_task.html",
        flag=True,
        tasks=crud.get_instoretask_by_id(task_id),
        technicians=crud.get_all_technicians(),
    )


@app.get("/admin/chiplevel")
def chiplevel():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("chiplevel.html",chiplevel=crud.get_all_chiplevel())

@app.post("/admin/chiplevel")
def chiplevel_filter():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "chiplevel.html",chiplevel=crud.get_all_chiplevel(filter=data))
    
    return redirect(url_for("chiplevel"))

@app.get("/admin/chiplevel/task/<task_id>")
def chiplevel_add(task_id):
    data = dict(request.form)
    admin = util.current_user_info(request)
    names = crud.get_all_partner_name()
    
    partner_name = data.get("partner_name")
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    

    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("chiplevel_add_task.html", flag=True,name=(name_lit), tasks=crud.get_instoretask_by_id(task_id),chiplevel=crud.get_chiplevel_by_id(task_id),partners=crud.get_all_partners())

@app.post("/admin/chiplevel/task/<task_id>")
def chiplevel_add_task(task_id):
    data = dict(request.form)
    names = crud.get_all_partner_name()
    
    partner_name = data.get("partner_name")
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    user = crud.get_partner(partner_name)
    if user:
        crud.update_chiplevel_task(data)
    else:
        error = "Partner Not Available"
        return render_template("chiplevel_add_task.html", 
                               flag=True,name=(name_lit),
                               errors=error, tasks=crud.get_instoretask_by_id(task_id),
                               chiplevel=crud.get_chiplevel_by_id(task_id),
                               partners=crud.get_all_partners())
    
    return render_template("chiplevel_add_task.html", 
                               flag=True,name=(name_lit),
                                tasks=crud.get_instoretask_by_id(task_id),
                               chiplevel=crud.get_chiplevel_by_id(task_id),
                               partners=crud.get_all_partners())


@app.get("/admin/warranty")
def warranty():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("warranty.html",warranty=crud.get_all_warranty())

@app.post("/admin/warranty")
def warranty_filter():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "warranty.html",warranty=crud.get_all_warranty(filter=data))
    
    return redirect(url_for("warranty"))

@app.get("/admin/warranty/task/<task_id>")
def warranty_add(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    names = crud.get_all_partner_name()
    names = crud.get_all_partner_name()
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    
    return render_template("warranty_add_task.html",flag=True,name=name_lit, tasks=crud.get_instoretask_by_id(task_id),warranty=crud.get_warranty_by_id(task_id),partners=crud.get_all_partners())

@app.post("/admin/warranty/task/<task_id>")
def warranty_update_task(task_id):
    data = dict(request.form)
    partner_name = data.get("partner_name")
    names = crud.get_all_partner_name()
    name_lit =[]
    for i in names:
        name_lit.append(i[0])
    user = crud.get_partner(partner_name)
    if user:
        crud.warranty_update_task(data)
    else:
        error = "Partner Not Available"
        return render_template("warranty_add_task.html",flag=True,name=name_lit,errors=error, tasks=crud.get_instoretask_by_id(task_id),warranty=crud.get_warranty_by_id(task_id),partners=crud.get_all_partners())

    return redirect("/admin/warranty/task/"+task_id)

@app.get("/admin/expenditure")
def expenditure():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    return render_template("expenditure.html")

@app.post("/admin/expenditure")
def expenditure_post():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    names = request.form.getlist('name[]')
    ages = request.form.getlist('age[]')

    # Process the received data here
    # You can perform any necessary operations on the data (e.g., store it in a database)

    # Example: Print the received data
    for name, age in zip(names, ages):
        print("Name:", name)
        print("Age:", age)
        print("---")

    return "Data received and processed successfully"



@app.get("/admin/order")
def order():
    admin = util.current_user_info(request)
    test = ['arrived','pending','completed','cancelled','all']
    test = json.dumps(test)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("order.html",customers=crud.get_all_customer(),test=test)


@app.get("/admin/followup")
def follow_up():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("follow_up.html")


@app.get("/admin/quotation")
def quotation():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("quotation.html", quotation=crud.get_all_quotation())


@app.post("/admin/quotation")
def quotation_create():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
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

#####WORK#######
@app.get("/admin/work")
def work():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "work.html",tasks=crud.get_work_all()
    )

@app.post("/admin/work")
def work_filter():
    data = dict(request.form)
    
    if data.get("ftype"):
        return render_template(
            "work.html",tasks=crud.get_work_all(filter=data))
    return render_template(
        "work.html",tasks=crud.get_work_all(filter=data)
    )

############# PDF GENERATION #####################

@app.route('/download/onsite/report/pdf/<task_id>')
def onsite_download_report(task_id):
    try:
        task = crud.get_onsitetask_by_id(task_id)
        resources=crud.get_resources_by_id(task_id)
        
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
        #pdf.image(name, x = None, y = None, w = 0, h = 0, type = '', link = '')

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(10)
        
        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 0.0, 'COM CARE SERVICES', align='C')
        pdf.ln(10)

        pdf.set_font('Times','B',18) 
        pdf.cell(page_width, 0.0, 'SERVICE REPORT', align='C')
        pdf.ln(20)
        
        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id)+'                                                                             Date: '+str(task.date), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Customer Name: '+str(task.customer.name)+'                                                          Phone no:'+str(task.customer.phone_no), align='L')
        pdf.ln(10)


        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Service Engineer: '+str(task.technician.name), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Service Type: '+str(task.service_type), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Service Status: '+str(task.status), align='L')
        pdf.ln(10)


        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Service Problem: '+str(task.problem), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Materials Changed: '+str(resources.material), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Service Changes: '+str(resources.service_charge), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Recived Amount: '+str(resources.received_charge), align='L')
        pdf.ln(10)

        pdf.set_font('Arial', '', 14)
        pdf.cell(page_width, 0.0, 'Remarks: '+str(resources.review), align='L')
        pdf.ln(20)


        pdf.ln(10)
        pdf.set_font('Arial','',14) 
        pdf.cell(page_width, 0.0, '                                                                               For com care', align='C')

        print('pdf created')
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
   
@app.route('/download/instore/report/pdf/<task_id>')
def instore_download_report(task_id):
    
    try:
        task = crud.get_instoretask_by_id(task_id)
        
        pdf = FPDF(orientation = 'p', unit = 'mm', format = 'A4')
        pdf.add_page()
         
        page_width = 180

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(0)

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(5)

        pdf.set_font('Times','',16) 
        pdf.cell(page_width, 10, 'SERVICE REPORT (Customer Copy)',  align='C')
        pdf.ln(20)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Date: '+str(task.date),ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Status: '+str(task.status),ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Customer Name: '+(str(task.customer.name)).capitalize(), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0,'Phone no:'+str(task.customer.phone_no),ln=3)
        pdf.ln(10)
    

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Est Days: '+str(task.est_days), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Est Charges: '+str(task.est_charge), align='L',ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Product Type: '+str(task.product.product_name), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Problem: '+str(task.problem).capitalize(), ln=3)
        pdf.ln(10)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Power Cable: '+str(task.power_cable).capitalize(), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Charger: '+str(task.charger).capitalize(), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Bag: '+str(task.bag).capitalize(), align='L', ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Product Details: '+str(task.product.product_company),align='L', ln=3)
        pdf.ln(0)


        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Other Items: '+str(task.items_received), ln=3)
        pdf.ln(10)


        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Service Charges: '+str(task.final_charge), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Advance/Recived Amt: '+str(task.recived_charge), ln=3)
        pdf.ln(10)

        #if task.status=="Delivered":
         #   pdf.set_font('Times','',15) 
          #  pdf.cell(page_width, 0.0, 'Deliverd on:'+str(task.delivery_date), align='L',ln=3)

        pdf.ln(15)
        pdf.set_font('Times','',15) 
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'For Com Care')

        pdf.ln(10)
        pdf.cell(0, 0.0, '-----------'*10)

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(20)

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(5)

        pdf.set_font('Times','',16) 
        pdf.cell(page_width, 10, 'SERVICE REPORT (Office Copy)',  align='C')
        pdf.ln(20)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Date: '+str(task.date),ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Status: '+str(task.status),ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Customer Name: '+(str(task.customer.name)).capitalize(), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0,'Phone no:'+str(task.customer.phone_no),ln=3)
        pdf.ln(10)
    

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Est Days: '+str(task.est_days), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Est Charges: '+str(task.est_charge), align='L',ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Product Type: '+str(task.product.product_name), align='L',ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Problem: '+str(task.problem).capitalize(), ln=3)
        pdf.ln(10)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Power Cable: '+str(task.power_cable).capitalize(), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(82)
        pdf.cell(page_width, 0.0, 'Charger: '+str(task.charger).capitalize(), ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Bag: '+str(task.bag).capitalize(), align='L', ln=3)
        pdf.ln(10)

        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Product Details: '+str(task.product.product_company),align='L', ln=3)
        pdf.ln(0)


        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Other Items: '+str(task.items_received), ln=3)
        pdf.ln(10)


        pdf.set_font('Times', '', 15)
        pdf.cell(page_width, 0.0, 'Service Charges: '+str(task.final_charge), align='L', ln=3)
        pdf.ln(0)

        pdf.set_font('Times', '', 15)
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Advance/Recived Amt: '+str(task.recived_charge), ln=3)
        pdf.ln(10)

        #if task.status=="Delivered":
         #   pdf.set_font('Times','',15) 
          #  pdf.cell(page_width, 0.0, 'Deliverd on:'+str(task.delivery_date), align='L',ln=3)

        pdf.ln(15)
        pdf.set_font('Times','',15) 
        pdf.set_x(135)
        pdf.cell(page_width, 0.0, 'Customer Sign')



        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=employee_report.pdf'})
    except Exception as e:
        print(e)

@app.route('/download/instore/day/report/pdf')
def instore_download_daily_report():
    
    try:
        
        date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%d/%m/%y")
        open_date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%y/%m/%d")
        current_date = open_date
        task = crud.get_instoretask_by_open_date(open_date)
        count_task = len(task)
        close_date = crud.get_instoretask_by_close_date(current_date)
        count_close_task = len(close_date)
        delviery_date = crud.get_instoretask_by_delivery_date(current_date)
        count_delivery_task = len(delviery_date)


        o_task = crud.get_instoretask_by_not_open_date(open_date)
        count_o_task = len(o_task)
        
        
       
        pdf = FPDF(orientation = 'p', unit = 'mm', format = 'A4')
        pdf.add_page()
         
        page_width = 180

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(0)

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(10)

        pdf.set_font('Times','B',15)
        pdf.cell(page_width, 0.0, 'Instore Daily Report', align='C')
        pdf.ln(10)

        col_width = page_width/6


        pdf.set_font('Times','B',13)
        pdf.cell(page_width,10,'Task Created on ' +str(date)+' - '+str(count_task),align='L')
        pdf.ln(10)

        pdf.set_font('Times','B',13)
        pdf.cell(13, 10, 'ID', border=1)
        pdf.cell(28, 10, 'Date', border=1)
        pdf.cell(45, 10, 'Customer Name', border=1)
        pdf.cell(23, 10, 'Type', border=1)
        pdf.cell(25, 10, 'Engineer', border=1)
        pdf.cell(col_width,10,  'Product Type',border=1)
        
        pdf.cell(col_width,10,  'Problem',border=1)
        pdf.ln(10)

        if count_task == 0:
            pdf.set_font('Times','B',13)
            pdf.cell(194,10,'No Task Created on ' +str(date),border=1,align='C')
            pdf.ln(10)
        for row in task:

            pdf.set_font('Times','',12)
            pdf.cell(13, 10, str(row.task_id), border=1)
            pdf.cell(28, 10, str(row.date), border=1)
            pdf.cell(45, 10, str(row.customer.name), border=1)
            pdf.cell(23, 10, str(row.service_type), border=1)
            pdf.cell(25, 10, str(row.technician.name), border=1)
            pdf.cell(30, 10, str(row.product.product_name), border=1)
            
            pdf.cell(col_width,10,str(row.problem),border=1)
            pdf.ln(10)

        
        pdf.set_font('Times','B',13)
        pdf.cell(page_width,10,'Task Completed on ' +str(date)+' - '+str(count_close_task),align='L')
        pdf.ln(10)

        pdf.set_font('Times','B',13)
        pdf.cell(13, 10, 'ID', border=1)
        pdf.cell(28, 10, 'Date', border=1)
        pdf.cell(45, 10, 'Customer Name', border=1)
        pdf.cell(23, 10, 'Type', border=1)
        pdf.cell(25, 10, 'Engineer', border=1)
        pdf.cell(col_width,10,  'Product Type',border=1)
        
        pdf.cell(col_width,10,  'Problem',border=1)
        pdf.ln(10)

        if count_close_task == 0:
            pdf.set_font('Times','B',13)
            pdf.cell(194,10,'No Task Created on ' +str(date),border=1,align='C')
            pdf.ln(10)
        

        for row in close_date:

            pdf.set_font('Times','',12)
            pdf.cell(13, 10, str(row.task_id), border=1)
            pdf.cell(28, 10, str(row.open_date), border=1)
            pdf.cell(45, 10, str(row.customer.name), border=1)
            pdf.cell(23, 10, str(row.service_type), border=1)
            pdf.cell(25, 10, str(row.technician.name), border=1)
            pdf.cell(30, 10, str(row.product.product_name), border=1)
            
            pdf.cell(col_width,10,str(row.problem),border=1)
            pdf.ln(10)


        pdf.set_font('Times','B',13)
        pdf.cell(page_width,10,'Task Delivered on ' +str(date)+' - '+str(count_delivery_task),align='L')
        pdf.ln(10)

        pdf.set_font('Times','B',13)
        pdf.cell(13, 10, 'ID', border=1)
        pdf.cell(28, 10, 'Date', border=1)
        pdf.cell(45, 10, 'Customer Name', border=1)
        pdf.cell(23, 10, 'Type', border=1)
        pdf.cell(25, 10, 'Engineer', border=1)
        pdf.cell(col_width,10,  'Product Type',border=1)
        
        pdf.cell(col_width,10,  'Problem',border=1)
        pdf.ln(10)

        if count_delivery_task == 0:
            pdf.set_font('Times','B',13)
            pdf.cell(194,10,'No Task Created on ' +str(date),border=1,align='C')
            pdf.ln(10)
        
        for row in delviery_date:

            pdf.set_font('Times','',12)
            pdf.cell(13, 10, str(row.task_id), border=1)
            pdf.cell(28, 10, str(row.open_date), border=1)
            pdf.cell(45, 10, str(row.customer.name), border=1)
            pdf.cell(23, 10, str(row.service_type), border=1)
            pdf.cell(25, 10, str(row.technician.name), border=1)
            
            pdf.cell(30, 10, str(row.product.product_name), border=1)
            
            pdf.cell(col_width,10,str(row.problem),border=1)
            pdf.ln(10)



        


        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=day_report.pdf'})
    except Exception as e:
        print(e)

@app.route('/download/instore/pemding/report/pdf')
def instore_download_pending_report():
    
    try:
        
        date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%d/%m/%y")
        open_date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%y/%m/%d")
        current_date = open_date
        task = crud.get_instoretask_by_open_date(open_date)
        count_task = len(task)
        close_date = crud.get_instoretask_by_close_date(current_date)
        count_close_task = len(close_date)
        delviery_date = crud.get_instoretask_by_delivery_date(current_date)
        count_delivery_task = len(delviery_date)


        o_task = crud.get_instoretask_by_not_open_date(open_date)
        count_o_task = len(o_task)
        
        
       
        pdf = FPDF(orientation = 'p', unit = 'mm', format = 'A4')
        pdf.add_page()
         
        page_width = 180

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(0)

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(10)

        pdf.set_font('Times','B',15)
        pdf.cell(page_width, 0.0, 'Instore Task Pending', align='C')
        pdf.ln(10)

        col_width = page_width/6


        
        pdf.set_font('Times','B',13)
        pdf.cell(page_width,10,'Task Pending'+' - '+str(count_o_task) ,align='L')
        pdf.ln(10)

        pdf.set_font('Times','B',13)
        pdf.cell(13, 10, 'ID', border=1)
        pdf.cell(28, 10, 'Date', border=1)
        pdf.cell(45, 10, 'Customer Name', border=1)
        pdf.cell(23, 10, 'Type', border=1)
        pdf.cell(25, 10, 'Engineer', border=1)
        pdf.cell(col_width,10,  'Product Type',border=1)
        
        pdf.cell(col_width,10,  'Problem',border=1)
        pdf.ln(10)

        if count_o_task == 0:
            pdf.set_font('Times','B',13)
            pdf.cell(194,10,'No Task Created on ' +str(date),border=1,align='C')
            pdf.ln(10)
        
        for row in o_task:

            pdf.set_font('Times','',12)
            pdf.cell(13, 10, str(row.task_id), border=1)
            pdf.cell(28, 10, str(row.open_date), border=1)
            pdf.cell(45, 10, str(row.customer.name), border=1)
            pdf.cell(23, 10, str(row.service_type), border=1)
            pdf.cell(25, 10, str(row.technician.name), border=1)
            pdf.cell(30, 10, str(row.product.product_name), border=1)
            
            pdf.cell(col_width,10,str(row.problem),border=1)
            pdf.ln(10)



        pdf.set_font('Times','',16) 
        pdf.cell(page_width, 10,'dd'+open_date,  align='C')
        pdf.ln(20)
        


        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=pending_report.pdf'})
    except Exception as e:
        print(e)



@app.route('/download/engineer/work/report/pdf')
def work_report():
    
    try:
        
        date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%d/%m/%y")
        open_date = datetime.now(pytz.timezone('Asia/Kolkata')).date().strftime("%y/%m/%d")
        current_date = open_date
        work = crud.get_work_by_open_date(open_date)
        
        #technicians=crud.get_work_by_tech()
        #print(technicians)
        #tech_id = technicians.technician_id
        #work_tech = crud.get_work_by_tech(tech_id)
        #print(work_tech)


        count_work = len(work)
        
        
       
        pdf = FPDF(orientation = 'p', unit = 'mm', format = 'A4')
        pdf.add_page()
         
        page_width = 180

        pdf.set_font('Times','B',30) 
        pdf.cell(page_width, 0.0, '', align='C')
        pdf.ln(0)
        

        pdf.set_font('Times','B',20) 
        pdf.cell(page_width, 5, 'COM CARE SERVICES', align='C')
        pdf.ln(10)

        pdf.set_font('Times','B',15)
        pdf.cell(page_width, 0.0, 'Onsite Work Completed', align='C')
        pdf.ln(10)

        col_width = page_width/6


        
        pdf.set_font('Times','B',13)
        pdf.cell(page_width,10,'Work Completed'+' - '+str(count_work) ,align='L')
        pdf.ln(10)

        pdf.set_font('Times','B',13)
        pdf.cell(13, 10, 'ID', border=1)
        pdf.cell(28, 10, 'Date', border=1)
        pdf.cell(45, 10, 'Customer Name', border=1)
        pdf.cell(23, 10, 'Type', border=1)
        pdf.cell(25, 10, 'Engineer', border=1)
        
        pdf.cell(col_width,10,  'Problem',border=1)
        pdf.ln(10)

        if count_work == 0:
            pdf.set_font('Times','B',13)
            pdf.cell(194,10,'No Task Created on ' +str(date),border=1,align='C')
            pdf.ln(10)
        
        for row in work:

            pdf.set_font('Times','',12)
            pdf.cell(13, 10, str(row.work_id), border=1)
            pdf.cell(28, 10, str(row.service_date), border=1)
            pdf.cell(45, 10, str(row.customer_name), border=1)
            pdf.cell(23, 10, str(row.service_type), border=1)
            pdf.cell(25, 10, str(row.technician.name), border=1)
            
            pdf.cell(col_width,10,str(row.problem),border=1)
            pdf.ln(10)


        pdf.set_font('Times','',16) 
        pdf.cell(page_width, 10,'dd'+open_date,  align='C')
        pdf.ln(20)
        


        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=pending_report.pdf'})
    except Exception as e:
        print(e)
