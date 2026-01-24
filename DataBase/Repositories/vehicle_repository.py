from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel

class VehicleRepository(BaseRepository[CompanyVehiclesDbTableModel]):
    def __init__(self, db_session):
        super().__init__(db_session, CompanyVehiclesDbTableModel)

    async def add_vehicle(self, add_vehicle: CompanyVehiclesDbTableModel) -> CompanyVehiclesDbTableModel:
        return await self.add(add_vehicle)

    async def get_by_id(self, vehicle_id: int) -> CompanyVehiclesDbTableModel | None:
        return await self.get(vehicle_id)
    
    async def get_company_vehicles(self, company_id: int) -> list[CompanyVehiclesDbTableModel]:
        return await self.filter(company_id=company_id)
    
    async def update_vehicle(self, vehicle: CompanyVehiclesDbTableModel) -> CompanyVehiclesDbTableModel:
        await self._commit()
        return vehicle
    