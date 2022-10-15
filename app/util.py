from app.views.admin import technician
from . import crud
from flask import request, url_for


def is_valid_password(username, password, role):
    if crud.get_password(username, role) == password:
        return True
    else:
        return False


def is_username_available(username: str, role: str) -> bool:
    if role == "admin":
        user = crud.get_admin(username)
    else:
        user = crud.get_technician(username)
    if user:
        return True
    return False

def is_customer_available(phone_no: str) -> bool:
    user = crud.get_customer_by_phone(phone_no)
    if user:
        return  True
    return False

def is_task_available(task_id: int) -> bool:
    task = crud.get_task_by_id(task_id)
    if task==None:
        return False
    else:
        return True