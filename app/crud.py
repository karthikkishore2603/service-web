from . import db, models, util
from datetime import datetime


def get_password(username: str, role: str) -> str:
    if role == "admin":
        password = models.Admin.query.filter_by(username=username).first()
    else:
        password = models.Technician.query.filter_by(username=username).first()

    if password:
        return password.password
    else:
        return None


def create_admin(data: dict) -> None:
    errors = ""
    if util.is_username_available(data["username"], "admin"):
        errors = "Username already exists,"

    if errors:
        raise Exception(errors)

    user = models.Admin(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()


def create_technician(data: dict) -> None:
    errors = ""
    if util.is_username_available(data["username"], "technician"):
        errors += "Username already exists,"

    if not util.is_phone_valid(data["phone_no"]):
        errors += "Invalid phone number,"

    if errors:
        raise Exception(errors[:-1])

    user = models.Technician(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()


def get_all_technicians(filter: dict = None) -> list:
    technicians = models.Technician.query
    if filter:
        if filter["ftechnician"]:
            technicians = technicians.filter_by(name=filter["ftechnician"])    
    technicians = technicians.all()
    return technicians



def get_all_admins() -> list:
    admins = models.Admin.query.all()
    return admins


def create_partners(data: dict) -> None:
    
    errors = ""
    if util.is_partner_available(data["partner_name"]):
        errors = "Username already exists,"

    if errors:
        raise Exception(errors[:-1])

    user = models.Partners(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()

def get_all_partners(filter: dict = None) -> list:
    partners = models.Partners.query
    if filter:
        if filter["fpartner"]:
            partners = partners.filter_by(partner_name=filter["fpartner"])
    return partners


def get_all_onsitetasks(filter: dict = None) -> list:
    tasks = models.OnsiteTask.query.order_by(models.OnsiteTask.date.desc())
    if filter:
        if filter.get("fphone"):
            customer = get_customer_by_phone(filter["fphone"])
            if customer:
                customer_id = customer.customer_id
                tasks = tasks.filter_by(customer_id=customer_id)
            else:
                tasks = tasks.filter_by(customer_id=None)
        if filter["fid"]:
            tasks = tasks.filter_by(task_id=filter["fid"])
        if filter["fdate"]:
            tasks = tasks.filter_by(date=filter["fdate"])
        if filter["fstype"]:
            tasks = tasks.filter_by(service_type=filter["fstype"])
        if filter["fstatus"]:
            tasks = tasks.filter_by(status=filter["fstatus"])
        
        if filter["ftechnician"]:
            tech_id=get_technician_id_by_name(filter["ftechnician"])
            if tech_id:
                tasks = tasks.filter_by(technician_id=tech_id[0])
            else:
                tasks = tasks.filter_by(technician_id=None)
    tasks = tasks.all()
    return tasks
    
def get_technicians(username: str) -> list:
    technicians = models.Technician.query.filter_by(username=username).all()
    return technicians


def get_technician_id_by_name(name: str) -> int:
    technician = models.Technician.query.filter_by(name=name).first()
    if technician:
        return technician.technician_id, technician.username
    else:
        return None


def get_technician_by_id(technician_id: int) -> models.Technician:
    return models.Technician.query.filter_by(technician_id=technician_id).first()


def get_onsitetask_by_id(task_id) -> models.OnsiteTask:
    return models.OnsiteTask.query.filter_by(task_id=task_id).first()


def get_onsitetask_by_tech_id(technician_id) -> models.OnsiteTask:
    return (
        models.OnsiteTask.query.filter_by(technician_id=technician_id).all()
        + models.OnsiteTask.query.filter_by(technician_id_2=technician_id).all()
        
    )

def get_instore_by_tech_id(technician_id) -> models.InstoreTask:
    return (
        models.InstoreTask.query.filter_by(technician_id=technician_id).all()
        
    )


def get_partner_by_id(partner_id) -> models.Chiplevel:
    return (
        models.Chiplevel.query.filter_by(partner_id=partner_id).all()+
        models.Warranty.query.filter_by(partner_id=partner_id).all()
        
    )

def get_onsitetask_by_cust_id(customer_id) -> models.OnsiteTask:
    return (models.OnsiteTask.query.filter_by(customer_id=customer_id).all())

def get_instoretask_by_cust_id(customer_id) -> models.InstoreTask:
    return (models.InstoreTask.query.filter_by(customer_id=customer_id).all())

def update_onsitetasks(data) -> list:
    errors = ""

    if not util.is_service_charge_valid(data["service_charge"]):
        errors += "Invalid Charges,"

    if not util.is_received_charge_valid(data["received_charge"]):
        errors += "Invalid Received Charges,"

    if errors:
        raise Exception(errors[:-1])

    if util.is_task_rsources_available(data["task_id"]):
        task_id = data.pop("task_id")
        db.session.query(models.Resources).filter(
            models.Resources.task_id == task_id
        ).update(data)
        db.session.commit()
        db.session.flush()
    else:
        update_tasks = models.Resources(**data)
        db.session.add(update_tasks)
        db.session.commit()
        db.session.flush()


def update_onsite_task_status(task_id: int) -> bool:
    task = get_onsitetask_by_id(task_id)
    if task and (task.status == "Pending"):
        task.status = "Completed"
        db.session.commit()
        db.session.flush()
        return True
    else:
        return False


def get_resources_by_id(task_id: int) -> models.Resources:
    return models.Resources.query.filter_by(task_id=task_id).first()


def get_resources_by_tech_id(tech: int) -> models.Resources:
    return models.Resources.query.filter_by(technician_id=tech).first()


def get_admin(username: str) -> models.Admin:
    return models.Admin.query.filter_by(username=username).first()

def get_partner(partner_name: str) -> models.Partners:
    partners = models.Partners.query.filter_by(partner_name=partner_name).first()
    if partners:
        return partners.partner_id

def get_admin_by_id(admin_id: int) -> models.Admin:
    return models.Admin.query.filter_by(admin_id=admin_id).first()


def get_technician(username: str) -> models.Technician:
    return models.Technician.query.filter_by(username=username).first()


def create_task(data: dict) -> None:
    errors = ""
    
    if not util.is_phone_valid(data["phone_no"]):
        errors += "Invalid phone number,"

    if errors:
        raise Exception(errors[:-1])

    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
            "address": data.pop("address"),
        }
    )
    
    if not util.is_customer_available(customer_data["phone_no"]):
        create_customer(customer_data)
    data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id
    task = models.OnsiteTask(creation_date=datetime.now(), **data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()


def create_instore_task(data: dict) -> None:
    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
        }
    )

    if not util.is_customer_available(customer_data["phone_no"]):
        create_customer(customer_data)
    data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id

    product_detail = {}
    product_detail.update(
        {
            "product_name": data.pop("product_name"),
            "product_company": data.pop("product_company"),
        }
    )

    if not util.is_product_available(product_detail["product_name"]):
        create_product(product_detail)
    data["product_id"] = get_product(product_detail["product_name"]).product_id

    data["est_days"] = int(data["est_days"]) if data["est_days"] else None
    data["est_charge"] = int(data["est_charge"]) if data["est_charge"] else None
    data["final_charge"] = int(data["final_charge"]) if data["final_charge"] else None
    data["recived_charge"] = int(data["recived_charge"]) if data["recived_charge"] else None

    task = models.InstoreTask(**data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()


def get_all_instoretasks(filter: dict = None) -> list:
    tasks = models.InstoreTask.query.order_by(models.InstoreTask.date.desc())
    if filter:
        if filter["fphone"]:
            customer = get_customer_by_phone(filter["fphone"])
            if customer:
                customer_id = customer.customer_id
                tasks = tasks.filter_by(customer_id=customer_id)
            else:
                tasks = tasks.filter_by(customer_id=None)
        if filter["fid"]:
            tasks = tasks.filter_by(in_task_id=filter["fid"])
        if filter["fdate"]:
            tasks = tasks.filter_by(date=filter["fdate"])
        if filter["fstype"]:
            tasks = tasks.filter_by(service_type=filter["fstype"])
        if filter["fstatus"]:
            tasks = tasks.filter_by(status=filter["fstatus"])
        
        if filter["ftechnician"]:
            tech_id=get_technician_id_by_name(filter["ftechnician"])
            if tech_id:
                tasks = tasks.filter_by(technician_id=tech_id[0])
            else:
                tasks = tasks.filter_by(technician_id=None)
                
    tasks = tasks.all()
    return tasks


def get_instoretask_by_id(in_task_id) -> models.InstoreTask:
    return models.InstoreTask.query.filter_by(in_task_id=in_task_id).first()


def update_instoretasks(data) -> list:
    if util.is_instore_task_available(data["in_task_id"]):

        customer_data = {}
        customer_data.update(
            {
                "name": data.pop("customer_name"),
                "phone_no": data.pop("phone_no"),
            }
        )

        if not util.is_customer_available(customer_data["phone_no"]):
            create_customer(customer_data)
        data["customer_id"] = get_customer_by_phone(
            customer_data["phone_no"]
        ).customer_id

        product_detail = {}
        product_detail.update(
            {
                "product_name": data.pop("product_name"),
                "product_company": data.pop("product_company"),
            }
        )

        if not util.is_product_available(product_detail["product_name"]):
            create_product(product_detail)
        data["product_id"] = get_product(product_detail["product_name"]).product_id

        in_task_id = data.pop("in_task_id")

        data["est_days"] = int(data["est_days"]) if data["est_days"] else None
        data["est_charge"] = int(data["est_charge"]) if data["est_charge"] else None
        data["final_charge"] = int(data["final_charge"]) if data["final_charge"] else None
        data["recived_charge"] = int(data["recived_charge"]) if data["recived_charge"] else None

        db.session.query(models.InstoreTask).filter(
            models.InstoreTask.in_task_id == in_task_id
        ).update(data)
        db.session.commit()
        db.session.flush()
    else:
        update_tasks = models.InstoreTask(**data)
        db.session.add(update_tasks)
        db.session.commit()
        db.session.flush()


def get_partnerid(partner_name: str) -> int:
    partner = models.Partners.query.filter_by(partner_name=partner_name).first()
    if partner:
        return partner.partner_id
    return None

def update_chiplevel_task(data: dict) -> None:
    

    if util.is_chiplevel_task_available(data["in_task_id"]):
        
        data["partner_id"] = get_partnerid(partner_name = data.pop("partner_name"))
        data["est_days"] = int(data["est_days"]) if data["est_days"] else None
        data["est_charge"] = int(data["est_charge"]) if data["est_charge"] else None
        data["partner_charge"] = int(data["partner_charge"]) if data["partner_charge"] else None
        data["recived_charge"] = int(data["recived_charge"]) if data["recived_charge"] else None

        in_task_id = data.pop("in_task_id")

        db.session.query(models.Chiplevel).filter(
            models.Chiplevel.in_task_id == in_task_id
        ).update(data)
        db.session.commit()
        db.session.flush()
    else:        
        data["partner_id"] = get_partnerid(partner_name = data.pop("partner_name"))
        data["est_days"] = int(data["est_days"]) if data["est_days"] else None
        data["est_charge"] = int(data["est_charge"]) if data["est_charge"] else None
        data["partner_charge"] = int(data["partner_charge"]) if data["partner_charge"] else None
        data["recived_charge"] = int(data["recived_charge"]) if data["recived_charge"] else None

        user = models.Chiplevel(**data)
        db.session.add(user)
        db.session.commit()
        db.session.flush()

def get_all_chiplevel(filter: dict = None) -> list:
    chiplevel = models.Chiplevel.query
    if filter:
        if filter["fid"]:
            chiplevel = chiplevel.filter_by(chiplevel_id=filter["fid"])
        if filter["fpartnername"]:
            partner_id = get_partner(filter["fpartnername"])
            if partner_id:
                chiplevel = chiplevel.filter_by(partner_id=partner_id)
            else:
                chiplevel = chiplevel.filter_by(partner_id=None)
        
    chiplevel = chiplevel.all()
    
    return chiplevel

def get_chiplevel_by_id(in_task_id) -> models.Chiplevel:
    return models.Chiplevel.query.filter_by(in_task_id=in_task_id).first()

def get_all_warranty(filter: dict = None) -> list:
    warranty = models.Warranty.query
    if filter:
        if filter["fid"]:
            warranty = warranty.filter_by(warranty_id=filter["fid"])
        if filter["fpartnername"]:
            partner_id = get_partner(filter["fpartnername"])
            if partner_id:
                warranty = warranty.filter_by(partner_id=partner_id)
            else:
                warranty = warranty.filter_by(partner_id=None)
        
    warranty = warranty.all()
    return warranty

def get_warranty_by_id(in_task_id) -> models.Warranty  :
    return models.Warranty.query.filter_by(in_task_id=in_task_id).first()

def get_onsite_count(status="Pending") -> int:
    return models.OnsiteTask.query.filter_by(status=status).count()

def get_instore_count_open(status="Open") -> int:
    return models.InstoreTask.query.filter_by(status=status).count()

def get_instore_count_pending(status="Closed") -> int:
    return models.InstoreTask.query.filter_by(status=status).count()

def get_chiplevel_count_sent(status="Sent") -> int:
    return models.Chiplevel.query.filter_by(status=status).count()

def get_warranty_count_sent(status="Sent") -> int:
    return models.Warranty.query.filter_by(status=status).count()

def warranty_update_task(data: dict) -> None:
    if util.is_warranty_task_available(data["in_task_id"]):
        
        data["partner_id"] = get_partnerid(partner_name = data.pop("partner_name"))

        data["est_days"] = int(data["est_days"]) if data["est_days"] else None

        in_task_id = data.pop("in_task_id")
        
        db.session.query(models.Warranty).filter(
            models.Warranty.in_task_id == in_task_id
        ).update(data)
        db.session.commit()
        db.session.flush()
    else:        
            
        data["partner_id"] = get_partnerid(partner_name = data.pop("partner_name"))

        data["est_days"] = int(data["est_days"]) if data["est_days"] else None
        
        user = models.Warranty(**data)
        db.session.add(user)
        db.session.commit()
        db.session.flush()

def get_customer_by_phone(phone_no: str) -> models.Customer:
    return models.Customer.query.filter_by(phone_no=phone_no).first()


def create_customer(data: dict) -> None:
    if util.is_customer_available(data["phone_no"]):
        print("hello")

    user = models.Customer(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()


def get_all_customer(filter: dict = None) -> list:
    customers = models.Customer.query
    if filter:
        if filter["fphone"]:
            customers = customers.filter_by(phone_no=filter["fphone"])
        
        if filter["fname"]:
            customers = customers.filter_by(name=filter["fname"])
    customers = customers.all()
    return customers


def get_product(product_name: str) -> models.Products:
    return models.Products.query.filter_by(product_name=product_name).first()


def create_product(data: dict) -> None:
    if util.is_product_available(data["product_name"]):
        print("hello")
    print(data)

    product = models.Products(**data)
    db.session.add(product)
    db.session.commit()
    db.session.flush()


def create_quotation(data: dict) -> None:
    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
            "address": data.pop("address"),
        }
    )

    if not util.is_customer_available(customer_data["phone_no"]):
        create_customer(customer_data)
    data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id

    quotation = models.Quotation(**data)
    db.session.add(quotation)
    db.session.commit()
    db.session.flush()


def get_all_quotation() -> list:
    quotation = models.Quotation.query.all()
    return quotation


# TECHNICIAN PAGE--------------------------------
def get_onsitetasks_by_tech(username: str, filter: dict = None) -> list:
    
    tasks = [
        models.OnsiteTask.query.filter(
            models.OnsiteTask.technician_id == models.Technician.technician_id,
            models.Technician.username == username,
        )
        , models.OnsiteTask.query.filter(
            models.OnsiteTask.technician_id_2 == models.Technician.technician_id,
            models.Technician.username == username,
        )
    ]

    if filter:
        if filter.get("fphone"):
            customer = get_customer_by_phone(filter["fphone"])
            if customer:
                customer_id = customer.customer_id
                tasks[0], tasks[1] = tasks[0].filter_by(customer_id=customer_id), tasks[1].filter_by(customer_id=customer_id)
            else:
                tasks[0], tasks[1] = tasks[0].filter_by(customer_id=None), tasks[1].filter_by(customer_id=None)
        if filter["fid"]:
            tasks[0], tasks[1] = tasks[0].filter_by(task_id=filter["fid"]), tasks[1].filter_by(task_id=filter["fid"])
        if filter["fdate"]:
            tasks[0], tasks[1] = tasks[0].filter_by(date=filter["fdate"]), tasks[1].filter_by(date=filter["fdate"])
        if filter["fstype"]:
            tasks[0], tasks[1] = tasks[0].filter_by(service_type=filter["fstype"]), tasks[1].filter_by(service_type=filter["fstype"])
        if filter["fstatus"]:
            tasks[0], tasks[1] = tasks[0].filter_by(status=filter["fstatus"]), tasks[1].filter_by(status=filter["fstatus"])
        
        if filter["ftechnician"]:
            tech_id=get_technician_id_by_name(filter["ftechnician"])
            if tech_id:
                tasks[0], tasks[1] = tasks[0].filter_by(technician_id=tech_id[0]), tasks[1].filter_by(technician_id_2=tech_id[0])
            else:
                tasks[0], tasks[1] = tasks[0].filter_by(technician_id=None), tasks[1].filter_by(technician_id_2=None)
    tasks = tasks[0].union(tasks[1]).all()
    return tasks

def get_instoretasks_by_tech(username: str, filter: dict = None) -> list:
    tasks = (
        models.InstoreTask.query.filter(
            models.InstoreTask.technician_id == models.Technician.technician_id,
            models.Technician.username == username,
        ).all()
        
    )

    return tasks