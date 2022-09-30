from email.policy import default
from logging import NullHandler
import string
from tokenize import Double
from .. import db
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship


class Admin(db.Model):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    phone_no = Column(String(20), nullable=False)


class Technician(db.Model):
    __tablename__ = "staff"
    staff_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    phone_no = Column(String(20), nullable=False)
    status = Column(Boolean)


class OnsiteTask(db.Model):
    __tablename__ = "onsite_task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer"))
    staff_id = Column(Integer, ForeignKey("staff"))
    service_type = Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)
    status = Column(String(20), default="open")
    review = Column(String(70), nullable=False)


class Resources(db.Model):
    __tablename__ = "resources"
    task_id = Column(Integer, ForeignKey("onsite_task"), primary_key=True)
    material = Column(String(20), nullable=False)
    service_charge = Column(Integer, nullable=True)
    received_charge = Column(Integer, nullable=True)


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    phone_no = Column(Integer, nullable=False)
    address = Column(String(25), nullable=False)


db.create_all()
