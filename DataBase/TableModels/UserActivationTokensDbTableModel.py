from sqlalchemy import String, ForeignKey, DateTime, Enum as SAEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .Base import Base
from datetime import datetime, timezone
from Enums.user_activation_stauts import UserActivationStatus

class UserActivationTokensDbTableModel(Base):
    __tablename__ = "user_activation_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer, nullable=False)
    activation_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[UserActivationStatus] = mapped_column(SAEnum(UserActivationStatus, name="user_activation_status"),
                                                         nullable=False)
    user: Mapped["UserDbTableModel"] = relationship(
        back_populates = "user_activation_link",
        lazy="selectin"
    )