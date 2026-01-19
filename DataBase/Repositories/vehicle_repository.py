from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel
from DataBase.TableModels.Vehicles.VehicleBodyTypesDbTableModel import VehicleBodyTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleLoadingTypesDbTableModel import VehicleLoadingTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleAdditionalOptionsDbTableModel import VehicleAdditionalOptionsDbTableModel
from typing import TypeVar, Type, Iterable
from Routes.Vehicles.vehicle_dto import CreateVehicleDTO

T = TypeVar("T")

ADDITIONAL_OPTIONS_ATTRIBUTE = 'additional_option'
BODY_TYPE_ATTRIBUTE = 'body_type'
LOADING_TYPE_ATTRIBUTE = 'loading_type'

class VehicleRepository(BaseRepository[CompanyVehiclesDbTableModel]):
    def __init__(self, db_session):
        super().__init__(db_session, CompanyVehiclesDbTableModel)

    async def add_vehicle(self, new_vehicle:CreateVehicleDTO) -> CompanyVehiclesDbTableModel:
        vehicle_data = new_vehicle.model_dump()
        vehicle_record = CompanyVehiclesDbTableModel(
            company_id= 1,  # to be replaced with actual company_id
            vehicle_type=vehicle_data.get('vehicle_type'),
            payload=vehicle_data.get('payload'),
            pallet_capacity=vehicle_data.get('pallet_capacity'),
            mark=vehicle_data.get('mark'),
            model=vehicle_data.get('model'),
            year=vehicle_data.get('year'),
            trailer=vehicle_data.get('trailer'),
            trailer_year=vehicle_data.get('trailer_year'),
            trailer_type=vehicle_data.get('trailer_type'),
            bitemp=vehicle_data.get('bitemp'),
            euro_class=vehicle_data.get('euro_class'),  
        )
        vehicle_record.body_types = self._map_list_fields(vehicle_data.get(BODY_TYPE_ATTRIBUTE),
                                                   VehicleBodyTypesDbTableModel, 
                                                    BODY_TYPE_ATTRIBUTE)
        vehicle_record.loading_types = self._map_list_fields(vehicle_data.get(LOADING_TYPE_ATTRIBUTE),
                                                      VehicleLoadingTypesDbTableModel, 
                                                      LOADING_TYPE_ATTRIBUTE)
        vehicle_record.additional_options = self._map_list_fields(vehicle_data.get(ADDITIONAL_OPTIONS_ATTRIBUTE),
                                                           VehicleAdditionalOptionsDbTableModel, 
                                                           ADDITIONAL_OPTIONS_ATTRIBUTE)
        created_vehicle = await self.add(vehicle_record)

        return created_vehicle
    
    def _map_list_fields(self, 
                         values: Iterable[str], 
                         model: Type[T], 
                         attribute_name: str) -> list[T]:
        if not values:
            return []
        return [model(**{attribute_name: value}) for value in values]

        