from . import db,models

def get_password(username: str) -> str:
    password=models.Admin.query.filter_by(username=username).first()
    if password!=None:
        return password.password
    else:
        return None