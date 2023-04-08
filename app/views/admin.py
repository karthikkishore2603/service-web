from flask import render_template, request, redirect, url_for, make_response,json,Response
import pymysql

from .. import app, crud, util, models, pdf
 #pip install flask-mysql
from fpdf import FPDF
 
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
            technicians=crud.get_all_technicians(filter=data)
            
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
    return render_template("partners.html", partners=crud.get_all_partners())

@app.post("/admin/partners")
def partners_add():
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "partners.html",
            partners=crud.get_all_partners(filter=data)
        )
    try:
        crud.create_partners(data)
    except Exception as e:
        return render_template(
            "partners.html",
            partners=crud.get_all_partners(),
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
    return render_template("customers.html", customers=crud.get_all_customer())

@app.post("/admin/customers")
def customers_filter():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "customers.html",
            customers=crud.get_all_customer(filter=data)
            
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


@app.route('/download/report/pdf/<task_id>')
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
   
@app.route('/download/report/pdf/<task_id>')
def instore_download_report(task_id):
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
    return render_template("instore.html", tasks=crud.get_all_instoretasks())

@app.post("/admin/instore")
def instore_filter_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    if data.get("ftype"):
        return render_template(
            "instore.html",
            tasks=crud.get_all_instoretasks(filter=data),
            technicians=crud.get_all_technicians(),
            
        )
    crud.create_task(data)

    return redirect(url_for("instore"))

@app.get("/admin/instore/add")
def instore_add_task():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "instore_add_task.html", technicians=crud.get_all_technicians(),tasks={}, flag=False
    )


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


@app.post("/admin/instore/add")
def instore_add_task_view():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    crud.create_instore_task(data)

    return redirect(url_for("instore"))


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
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template("chiplevel_add_task.html", flag=True, tasks=crud.get_instoretask_by_id(task_id),chiplevel=crud.get_chiplevel_by_id(task_id),partners=crud.get_all_partners())

@app.post("/admin/chiplevel/task/<task_id>")
def chiplevel_add_task(task_id):
    data = dict(request.form)
    try:
        crud.update_chiplevel_task(data)
    except Exception as e:
        print(e)
        return render_template("chiplevel_add_task.html",errors=str(e).split(","), flag=True, tasks=crud.get_instoretask_by_id(task_id),chiplevel=crud.get_chiplevel_by_id(task_id),partners=crud.get_all_partners())

    return redirect("/admin/chiplevel/task/"+task_id)


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
    return render_template("warranty_add_task.html",flag=True, tasks=crud.get_instoretask_by_id(task_id),warranty=crud.get_warranty_by_id(task_id),partners=crud.get_all_partners())

@app.post("/admin/warranty/task/<task_id>")
def warranty_update_task(task_id):
    data = dict(request.form)
    crud.warranty_update_task(data)
    return redirect("/admin/warranty/task/"+task_id)

@app.get("/admin/expenditure")
def expenditure():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
   
    return render_template("expenditure.html")


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
