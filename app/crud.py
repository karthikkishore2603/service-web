from . import db 

def get_password(username: str) -> str:
    password = db.Model.Admin.query.filter_by(username=username).first()
    print(password)
    return password