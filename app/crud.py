from . import db, models

def get_password(username: str,role) -> str:
    if role=="admin":
        password=models.Admin.query.filter_by(username=username).first()
    else:
        password=models.Technician.query.filter_by(username=username).first()
        
    if password!=None:
        return password.password
    else:
        return None

    
def create_user(data: dict, type: str) -> None:
    if type=="admin":
        user=models.Admin(**data)
    else:
        user=models.Technician(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()

def get_all_technicians() -> list:
    technicians=models.Technician.query.all()
    return technicians

def get_all_admins() -> list:
    admins=models.Admin.query.all()
    return admins

def create_task(data: dict) -> None:
    task=models.OnsiteTask(**data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()

def display_task() -> list:
    display_task=models.OnsiteTask.query.all()
    return display_task