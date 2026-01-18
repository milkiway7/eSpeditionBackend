from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime

class VehicleBodyTypesDbTableModel(Base):
    __tablename__ = 'vehicle_body_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('company_vehicles.id'), nullable=False)
    body_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # Relationships
    vehicle: Mapped["CompanyVehiclesDbTableModel"] = relationship(
        back_populates="body_types"
    )