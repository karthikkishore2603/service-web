from . import db,models,crud




def is_valid_password(username,password):
    if crud.get_password(username)==password:
        return True
    else:
        return False
