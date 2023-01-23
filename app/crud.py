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


def get_all_technicians() -> list:
    technicians = models.Technician.query.all()
    return technicians



def get_all_admins() -> list:
    admins = models.Admin.query.all()
    return admins


def create_partners(data: dict) -> None:
    """
    errors = ""
    if util.is_username_available(data["username"], "technician"):
        errors += "Username already exists,"

    if not util.is_phone_valid(data["phone_no"]):
        errors += "Invalid phone number,"

    if errors:
        raise Exception(errors[:-1])
"""
    user = models.Partners(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()

def get_all_partners() -> list:
    partners = models.Partners.query.all()
    return partners


def get_all_onsitetasks(filter: dict = None) -> list:
    tasks = models.OnsiteTask.query
    if filter:
        customer = get_customer_by_phone(filter["fphone"])
        if customer:
            customer_id = customer.customer_id
            tasks = tasks.filter_by(customer_id=customer_id)
        if filter["fid"]:
            tasks = tasks.filter_by(task_id=filter["fid"])
        if filter["fdate"]:
            tasks = tasks.filter_by(date=filter["fdate"])
        if get_technician_id_by_name(filter["ftechnician"]):
            tasks = tasks.filter_by(
                technician_id=get_technician_id_by_name(filter["ftechnician"])
            )
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
        + models.OnsiteTask.query.filter_by(technician_id_2=technician_id).all()+
        models.InstoreTask.query.filter_by(technician_id=technician_id).all()
        
    )


def get_onsitetask_by_cust_id(customer_id) -> models.OnsiteTask:
    return models.OnsiteTask.query.filter_by(customer_id=customer_id).all()


def update_onsitetasks(data) -> list:
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
    task = get_resources_by_id(task_id)
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


def get_admin_by_id(admin_id: int) -> models.Admin:
    return models.Admin.query.filter_by(admin_id=admin_id).first()


def get_technician(username: str) -> models.Technician:
    return models.Technician.query.filter_by(username=username).first()


def create_task(data: dict) -> None:
    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
            "address": data.pop("address"),
        }
    )
    if not util.is_phone_valid(customer_data["phone_no"]):
        raise Exception("Invalid phone number")
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


def get_all_instoretasks() -> list:
    tasks = models.InstoreTask.query.all()
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

def chiplevel_update_task(data: dict) -> None:
    partner_data = {}
    print(data)
    partner_data.update(
            {
                "name": data.pop("partner_name"),
                
            }
        )
    user = models.Chiplevel(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()

def warranty_update_task(data: dict) -> None:
    partner_data = {}
    print(data)
    partner_data.update(
            {
                "name": data.pop("partner_name"),
                
            }
        )
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


def get_all_customer() -> list:
    customers = models.Customer.query.all()
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
    tasks = (
        models.OnsiteTask.query.filter(
            models.OnsiteTask.technician_id == models.Technician.technician_id,
            models.Technician.username == username,
        ).all()
        + models.OnsiteTask.query.filter(
            models.OnsiteTask.technician_id_2 == models.Technician.technician_id,
            models.Technician.username == username,
        ).all()
    )

    return tasks
