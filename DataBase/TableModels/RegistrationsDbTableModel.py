from sqlalchemy import String, DateTime, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from Enums.registration_status import RegistrationStatus
from Enums.company_type import CompanyType


class RegistrationsDbTableModel(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint("registration_id", name="uq_registration_registration_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    registration_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nip: Mapped[str] = mapped_column(String(10), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    registration_status: Mapped[RegistrationStatus] = mapped_column(
        SAEnum(RegistrationStatus, name="registration_status"), nullable=False
    )
    company_type: Mapped[CompanyType | None] = mapped_column(
        SAEnum(CompanyType, name="company_type"), nullable=True
    )
    company_country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company_postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    company_street: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_building_number: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
    company_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
