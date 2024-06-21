from .extensions import db
from datetime import datetime
from enum import Enum


class Status(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.NEW, nullable=False)
