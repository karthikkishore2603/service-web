from . import db,models,crud,app


from flask import request, url_for



def is_valid_password(username,password,role):
    if crud.get_password(username,role)==password:
        return True
    else:
        return False
