from sqlalchemy import String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime
from Enums.roles import Role


class CompanyEmployeesDbTableModel(Base):
    __tablename__ = "company_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role"), nullable=False)
    # Relationships
    user: Mapped["UserDbTableModel"] = relationship(
        back_populates="company_links"
    )
    company: Mapped["CompaniesDbTableModel"] = relationship(    
        back_populates="user_links"
    )


