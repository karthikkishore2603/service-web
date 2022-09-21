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

db.create_all()