from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CompaniesDbTableModel(Base):
    __tablename__="companies"

    __table_args__ =(
        UniqueConstraint('nip', name='uq_company_nip'),
        UniqueConstraint('vat_eu', name='uq_company_vat_eu'),
        UniqueConstraint('company_name', name='uq_company_name'),
    )

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at= Column(DateTime, nullable=False)
    updated_at= Column(DateTime, nullable=True)
    nip= Column(String(10), nullable=False)
    vat_eu= Column(String(20), nullable=True)
    country= Column(String(50), nullable=False)
    city= Column(String(100), nullable=False)
    postal_code= Column(String(20), nullable=False)
    street= Column(String(100), nullable=False)
    building_number= Column(String(10), nullable=False)
    website= Column(String(100), nullable=True)
    phone_number= Column(String(15), nullable=False)
    company_name= Column(String(100), nullable=False)