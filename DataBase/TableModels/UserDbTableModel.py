from sqlalchemy import String, DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .Base import Base

class UserDbTableModel(Base):
    __tablename__ = "users"

    __table_args__ =(
        UniqueConstraint('email', name='uq_user_email'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    account_type: Mapped[str] = mapped_column(String(40), nullable=False)

    # Relationships
    company_links: Mapped[list["CompanyEmployeesDbTableModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )