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
    creation_date = Column(Date)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    technician_id = Column(Integer, ForeignKey("technician.technician_id"))
    technician_id_2 = Column(Integer, ForeignKey("technician.technician_id"))
    service_type = Column(String(20), nullable=False)
    problem = Column(String(20), nullable=False)

    technician = relationship("Technician", foreign_keys=[technician_id])
    technician2 = relationship("Technician", foreign_keys=[technician_id_2])
    customer = relationship("Customer")


class Resources(db.Model):
    __tablename__ = "resources"
    task_id = Column(Integer, ForeignKey("onsite_task"), primary_key=True)
    material = Column(String(20), nullable=False)
    service_charge = Column(Integer, nullable=True)
    received_charge = Column(Integer, nullable=True)
    status = Column(String(20), default="Pending")
    review = Column(String(70))


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    phone_no = Column(String(10), nullable=False)
    address = Column(String(25))


class InstoreTask(db.Model):
    __tablename__ = "instore_task"
    in_task_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    service_type = Column(String(20), nullable=False)
    status = Column(String(20))
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))

    product_id = Column(Integer, ForeignKey("product.product_id"))
    technician_id = Column(Integer, ForeignKey("technician"))
    chiplevel_id = Column(Integer, ForeignKey("chiplevel"))
    problem = Column(String(20), nullable=False)
    product_details = Column(String(20), nullable=False)

    est_days = Column(Integer)
    est_charge = Column(Integer)
    final_charge = Column(Integer)
    recived_charge = Column(Integer)
    remarks = Column(String(70))
    items_received = Column(String(70), nullable=False)
    serial_no = Column(String(70))

    technician = relationship("Technician")
    customer = relationship("Customer")
    product = relationship("Products")


class Products(db.Model):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(20), nullable=False)
    product_company = Column(String(20))


class Partners(db.Model):
    __tablename__ = "partners"
    partner_id = Column(Integer, primary_key=True, autoincrement=True)
    partner_name = Column(String(20), nullable=False)
    phone_no = Column(String(10), nullable=False)
    partner_address = Column(String(20))


class Chiplevel(db.Model):
    __tablename__ = "chiplevel"
    chiplevel_id = Column(Integer, primary_key=True, autoincrement=True)
    in_task_id = Column(Integer, ForeignKey("instoretask"))
    status = Column(String(20))
    outward_date = Column(Date, nullable=False)
    inward_date = Column(Date)
    est_days = Column(Integer)
    est_charge = Column(Integer)
    partner_charge = Column(Integer)
    recived_charge = Column(Integer)
    remarks = Column(String(70))
    items_sent = Column(String(70))
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))

    Partners = relationship("Partners")
    instoretask = relationship("InstoreTask")

class Warranty(db.Model):
    __tablename__ = "warranty"
    warranty_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(20))
    outward_date = Column(Date, nullable=False)
    inward_date = Column(Date, nullable=False)
    est_days = Column(Integer)
   
    work = Column(String(20))
    wtype = Column(String(20))
    remarks = Column(String(70))
    items_sent = Column(String(70))
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))

    Partners = relationship("Partners")

class Quotation(db.Model):
    __tablename__ = "quotation"
    quotation_no = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    customer = relationship("Customer")


db.create_all()
