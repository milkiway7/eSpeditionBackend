from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel

class VehicleRepository(BaseRepository[CompanyVehiclesDbTableModel]):
    def __init__(self, db_session):
        super().__init__(db_session, CompanyVehiclesDbTableModel)

    async def add_vehicle(self, add_vehicle: CompanyVehiclesDbTableModel) -> CompanyVehiclesDbTableModel:
        return await self.add(add_vehicle)

        