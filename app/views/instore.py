from flask import render_template, request, redirect, url_for, make_response,json,Response, jsonify, send_file
import pymysql
from .. import app, crud, util, models, pdf,db

from fpdf import FPDF
import pytz
from  .. import msgtest


@app.route('/admin/instorenew', methods=['GET', 'POST'])
def instorenew():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    
    instorenew = get_instorenew()
    
    return render_template('instorenew.html', instorenew=instorenew)

def add_instorenew(data: dict):
    instask = models.InstoreNew(**data)
    db.session.add(instask)
    db.session.commit()
    db.session.flush()

def get_instorenew():
    instorenew = models.InstoreNew.query.all()
    return instorenew

def get_instorenew_by_id(task_id):
    instorenew = models.InstoreNew.query.filter_by(task_id=task_id).first()
    return instorenew


@app.route('/admin/instorenew/add', methods=['GET', 'POST'])
def instorenew_add():
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    

    if request.method == 'POST':
        data = dict(request.form)
        
        add_instorenew(data)
        # msgtest.send_whatsapp_message(data)
        print(data)


    return render_template('instorenew_add.html', tasks = {""},technicians=crud.get_all_technicians())


@app.get("/admin/instorenew/task/<task_id>")
def instorenew_task_view_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    return render_template(
        "instorenew_add.html",
        flag=True,
        tasks=get_instorenew_by_id(task_id),technicians=crud.get_all_technicians()
    )


@app.post("/admin/instorenew/task/<task_id>")
def instorenew_task_update_by_id(task_id):
    admin = util.current_user_info(request)
    if not util.is_user_authenticated(request,type="admin") or not admin:
        return render_template("check.html")
    data = dict(request.form)
    task = get_instorenew_by_id(task_id)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return redirect(url_for("instorenew"))


@app.route('/download/instorenew/report/pdf/<task_id>')
def instorenew_download_report(task_id):
    
    try:
        task = get_instorenew_by_id(task_id)
        
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
        
        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id), ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(82)
        # pdf.cell(page_width, 0.0, 'Date: '+str(task.date),ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Status: '+str(task.status),ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Customer Name: '+(str(task.customer.name)).capitalize(), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0,'Phone no:'+str(task.customer.phone_no),ln=3)
        # pdf.ln(10)
    

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Est Days: '+str(task.est_days), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Est Charges: '+str(task.est_charge), align='L',ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Product Type: '+str(task.product.product_name), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Problem: '+str(task.problem).capitalize(), ln=3)
        # pdf.ln(10)
        
        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Power Cable: '+str(task.power_cable).capitalize(), align='L', ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(82)
        # pdf.cell(page_width, 0.0, 'Charger: '+str(task.charger).capitalize(), ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Bag: '+str(task.bag).capitalize(), align='L', ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Product Details: '+str(task.product.product_company),align='L', ln=3)
        # pdf.ln(0)


        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Other Items: '+str(task.items_received), ln=3)
        # pdf.ln(10)


        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Service Charges: '+str(task.final_charge), align='L', ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Advance/Recived Amt: '+str(task.recived_charge), ln=3)
        # pdf.ln(10)

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
        
        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Task ID: '+str(task.task_id), ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(82)
        # pdf.cell(page_width, 0.0, 'Date: '+str(task.date),ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Status: '+str(task.status),ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Customer Name: '+(str(task.customer.name)).capitalize(), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0,'Phone no:'+str(task.customer.phone_no),ln=3)
        # pdf.ln(10)
    

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Est Days: '+str(task.est_days), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Est Charges: '+str(task.est_charge), align='L',ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Product Type: '+str(task.product.product_name), align='L',ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Problem: '+str(task.problem).capitalize(), ln=3)
        # pdf.ln(10)
        
        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Power Cable: '+str(task.power_cable).capitalize(), align='L', ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(82)
        # pdf.cell(page_width, 0.0, 'Charger: '+str(task.charger).capitalize(), ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Bag: '+str(task.bag).capitalize(), align='L', ln=3)
        # pdf.ln(10)

        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Product Details: '+str(task.product.product_company),align='L', ln=3)
        # pdf.ln(0)


        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Other Items: '+str(task.items_received), ln=3)
        # pdf.ln(10)


        # pdf.set_font('Times', '', 15)
        # pdf.cell(page_width, 0.0, 'Service Charges: '+str(task.final_charge), align='L', ln=3)
        # pdf.ln(0)

        # pdf.set_font('Times', '', 15)
        # pdf.set_x(135)
        # pdf.cell(page_width, 0.0, 'Advance/Recived Amt: '+str(task.recived_charge), ln=3)
        # pdf.ln(10)

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
