from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBase.TableModels.Base import Base
from datetime import datetime

class VehicleAdditionalOptionsDbTableModel(Base):
    __tablename__ = 'vehicle_additional_options'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('company_vehicles.id'), nullable=False)
    additional_option: Mapped[str] = mapped_column(String(100), nullable=False)
    # Relationships
    vehicle: Mapped["CompanyVehiclesDbTableModel"] = relationship(
        back_populates="additional_options"
    )