from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class UserDbTableModel(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at= Column(DateTime, nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    password= Column(String(255), nullable=False)
    name= Column(String(50), nullable=False)
    surname= Column(String(50), nullable=False)
    phone_number= Column(Integer)

