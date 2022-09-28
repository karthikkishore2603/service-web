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
    __tablename__="admins"
    username=Column(String(20),primary_key=True)
    password=Column(String(20),nullable=False)
    name=Column(String(20),nullable=False)
    phone_no=Column(String(20),nullable=False)

class Technician(db.Model):
    __tablename__="technicians"
    username=Column(String(20),primary_key=True)
    password=Column(String(20),nullable=False)
    name=Column(String(20),nullable=False)
    phone_no=Column(String(20),nullable=False)

class OnsiteTask(db.Model):
    __tablename__="onsite_add_task"
    id=Column(Integer,primary_key=True)
    customer_name=Column(String(20),nullable=False)
    address=Column(String(20),nullable=False)
    phone_no=Column(String(20),nullable=False)   
    problem=Column(String(20),nullable=False)
    work=Column(String(20),nullable=False)
    date=Column(Date,nullable=False)
    technician=Column(String(20),nullable=False)
    service_charge=Column(Integer,nullable=True)
    received_charge=Column(Integer,nullable=True)


db.create_all()