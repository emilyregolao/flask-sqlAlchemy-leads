from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Lead(db.Model):

    id: int
    name: str
    email: str
    phone: str
    creation_date: datetime
    last_visit: datetime
    visits: int

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False)
    phone = Column(String,unique=True, nullable=False)
    creation_date = Column(DateTime,default=datetime.now())
    last_visit = Column(DateTime, default=datetime.now())
    visits = Column(Integer, default=1)