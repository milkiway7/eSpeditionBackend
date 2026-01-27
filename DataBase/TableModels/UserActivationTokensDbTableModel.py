from sqlalchemy import String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .Base import Base
from datetime import datetime, timezone

class UserActivationTokensDbTableModel(Base):
    __tablename__ = "user_activation_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    hash_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["UserDbTableModel"] = relationship(
        back_populates = "user_activation_link"
    )