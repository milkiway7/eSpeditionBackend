from sqlalchemy import String, ForeignKey, Enum as SAEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime, timezone

class CompanyEmployeesDbTableModel(Base):
    __tablename__ = "company_employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False, default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    # Relationships
    user: Mapped["UserDbTableModel"] = relationship(
        back_populates="company_employee_links"
    )
    company: Mapped["CompaniesDbTableModel"] = relationship(    
        back_populates="user_links"
    )


