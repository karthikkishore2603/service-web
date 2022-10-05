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
    __tablename__ = "technician"
    technician_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    phone_no = Column(String(20), nullable=False)
    status = Column(Boolean)


class OnsiteTask(db.Model):
    __tablename__ = "onsite_task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    technician_id = Column(Integer, ForeignKey("technician"))
    service_type = Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)
    

    customer = relationship("Customer")


class Resources(db.Model):
    __tablename__ = "resources"
    task_id = Column(Integer, ForeignKey("onsite_task"), primary_key=True)
    material = Column(String(20), nullable=False)
    service_charge = Column(Integer, nullable=True)
    received_charge = Column(Integer, nullable=True)
    status = Column(String(20), default="open")
    review = Column(String(70))

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    phone_no = Column(Integer, nullable=False)
    address = Column(String(25), nullable=False)


class InstoreTask(db.Model):
    __tablename__ = "instore_task"
    in_task_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    service_type = Column(String(20), nullable=False)
    product_details =Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)
    est_days = Column(Integer, nullable=True)
    est_charge = Column(Integer, nullable=True)
    remarks =Column(String(70), nullable=True)
    items = Column(Integer, ForeignKey("customer.customer_id"))


class Products(db.Model):
    __tablename__ = "product"
    in_task_id = Column(Integer, primary_key=True)
    product_name = Column(String(20), nullable=False)
    serial_no = Column(String(20))
    description = Column(String(70))
    nos = Column(Integer, nullable=False)







db.create_all()
