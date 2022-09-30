from . import db, models, util


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
    if util.is_username_available(data["username"], "admin"):
        errors = "Username already exists,"

    if errors:
        raise Exception(errors)

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

def get_all_onsitetasks() -> list:
    tasks = models.OnsiteTask.query.all()
    return tasks

def get_admin(username: str) -> models.Admin:
    return models.Admin.query.filter_by(username=username).first()


def get_technician(username: str) -> models.Technician:
    return models.Technician.query.filter_by(username=username).first()


def create_task(data: dict) -> None:
    task = models.OnsiteTask(**data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()
