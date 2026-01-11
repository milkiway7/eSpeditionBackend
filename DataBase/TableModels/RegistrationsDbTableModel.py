from sqlalchemy import String, DateTime, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from Enums.registration_status import RegistrationStatus
from Enums.account_type import AccountType

Base = declarative_base()

class RegistrationsDbTableModel(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint('registration_id', name='uq_registration_registration_id'),
        UniqueConstraint('email', name='uq_registration_email'),
        UniqueConstraint('nip', name='uq_registration_nip'),
        UniqueConstraint('user_phone', name='uq_registration_user_phone'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    registration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),nullable=False, default=uuid.uuid4)
    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at:Mapped[datetime | None] = mapped_column(DateTime, nullable=True, onupdate=datetime.now)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nip: Mapped[str] = mapped_column(String(10), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    registration_status: Mapped[RegistrationStatus] = mapped_column(SAEnum(RegistrationStatus), nullable=False)
    account_type: Mapped[AccountType | None] = mapped_column(SAEnum(AccountType), nullable=True)
