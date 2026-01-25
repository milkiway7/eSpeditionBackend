from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime

class CompanyVehiclesDbTableModel(Base):
    __tablename__ = "company_vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, onupdate=datetime.now)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[int] = mapped_column(Integer,nullable=False)
    pallet_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    mark: Mapped[str] = mapped_column(String(100), nullable=True)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    trailer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    trailer_year: Mapped[int] = mapped_column(Integer, nullable=True)
    trailer_type: Mapped[str] = mapped_column(String(100), nullable=True)
    bitemp: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    euro_class: Mapped[str] = mapped_column(String(100), nullable=False)

    #Relationships
    company: Mapped["CompaniesDbTableModel"] = relationship(
        back_populates= "company_vehicles"
    )
    body_types: Mapped[list["VehicleBodyTypesDbTableModel"]] = relationship(
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    loading_types: Mapped[list["VehicleLoadingTypesDbTableModel"]] = relationship(
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    additional_options: Mapped[list["VehicleAdditionalOptionsDbTableModel"]] = relationship(
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin"
    )