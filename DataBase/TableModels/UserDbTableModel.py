from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class UserDbTableModel(Base):
    __tablename__="users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at= Column(DateTime, nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    password= Column(String(255), nullable=False)
    name= Column(String(50), nullable=False)
    surname= Column(String(50), nullable=False)
    phone= Column(Integer)

