from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime, timezone

class VehicleLoadingTypesDbTableModel(Base):
    __tablename__ = 'vehicle_loading_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('company_vehicles.id'), nullable=False)
    loading_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    vehicle: Mapped["CompanyVehiclesDbTableModel"] = relationship(
        back_populates="loading_types"
    )