from sqlalchemy import (String, DateTime,
                        UniqueConstraint, Boolean, 
                        Enum as SAEnum, CheckConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .Base import Base
from Enums.user_roles import UserRoles

class UserDbTableModel(Base):
    __tablename__ = "users"

    __table_args__ =(
        UniqueConstraint('email', name='uq_user_email'),
        CheckConstraint(
            "(is_active = false AND password IS NULL) OR "
            "(is_active = true AND password IS NOT NULL AND name IS NOT NULL AND surname IS NOT NULL AND phone_number IS NOT NULL)",
            name="chk_user_password_active"
        )
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc)
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    surname: Mapped[str] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    user_role: Mapped[UserRoles] = mapped_column(SAEnum(UserRoles, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # Relationships
    company_employee_links: Mapped[list["CompanyEmployeesDbTableModel"]] = relationship(
        back_populates="user", # Users.company_links[i].user <-> ten sam User. Zmiana po jednej stronie widoczna w drugiej
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    user_activation_link: Mapped[list["UserActivationTokensDbTableModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
