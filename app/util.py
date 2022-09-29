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
