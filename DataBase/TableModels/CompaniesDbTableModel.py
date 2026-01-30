from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .Base import Base

class CompaniesDbTableModel(Base):
    __tablename__="companies"

    __table_args__ =(
        UniqueConstraint('nip', name='uq_company_nip'),
        UniqueConstraint('name', name='uq_company_name'),
    )

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    updated_at:Mapped[datetime]= mapped_column(DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))
    nip:Mapped[str]= mapped_column(String(10), nullable=False)
    name:Mapped[str]= mapped_column(String(200), nullable=False)
    country:Mapped[str]= mapped_column(String(50), nullable=False)
    city:Mapped[str]= mapped_column(String(100), nullable=False)
    postal_code:Mapped[str]= mapped_column(String(20), nullable=False)
    street:Mapped[str]= mapped_column(String(100), nullable=False)
    building_number:Mapped[str]= mapped_column(String(10), nullable=False)
    email:Mapped[str]= mapped_column(String(100), nullable=True)
    phone_number:Mapped[str]= mapped_column(String(15), nullable=False)
    company_type: Mapped[str] = mapped_column(String(40), nullable=False)

    user_links: Mapped[list["CompanyEmployeesDbTableModel"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    company_vehicles: Mapped[list["CompanyVehiclesDbTableModel"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin"
    )