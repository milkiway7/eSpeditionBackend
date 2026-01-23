from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel
from DataBase.TableModels.Vehicles.VehicleBodyTypesDbTableModel import VehicleBodyTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleLoadingTypesDbTableModel import VehicleLoadingTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleAdditionalOptionsDbTableModel import VehicleAdditionalOptionsDbTableModel
from DataBase.Repositories.vehicle_repository import VehicleRepository
from typing import TypeVar, Type, Iterable
from Exceptions.domain_exceptions import UnauthorizedError
from Routes.Vehicles.vehicle_dto import ReadVehicleDTO, CreateVehicleDTO
from Exceptions.domain_exceptions import UnauthorizedError
from Enums.user_roles import UserRoles

T = TypeVar("T")

ADDITIONAL_OPTIONS_ATTRIBUTE = 'additional_option'
BODY_TYPE_ATTRIBUTE = 'body_type'
LOADING_TYPE_ATTRIBUTE = 'loading_type'

class VehicleService:
    def __init__(self, repo: VehicleRepository):
        self.repo = repo

    async def create_vehicle(
        self,
        dto: CreateVehicleDTO,
        user: dict,
    ) -> ReadVehicleDTO:
        if user["company_type"] != "CARRIER":
            raise UnauthorizedError("Unauthorized access. To add a vehicle, user must have CARRIER account type.")
        if user["user_role"] not in [UserRoles.CARRIER_ADMIN.value, UserRoles.CARRIER_SPEDITOR.value]:
            raise UnauthorizedError("Unauthorized access. To add a vehicle, user must have SPEDITOR or ADMIN role.")
        
        vehicle = CompanyVehiclesDbTableModel(
            company_id=user["company_id"],
            vehicle_type=dto.vehicle_type,
            payload=dto.payload,
            pallet_capacity=dto.pallet_capacity,
            mark=dto.mark,
            model=dto.model,
            year=dto.year,
            trailer=dto.trailer,
            trailer_year=dto.trailer_year,
            trailer_type=dto.trailer_type,
            bitemp=dto.bitemp,
            euro_class=dto.euro_class,
        )

        vehicle.body_types = self._map_list_fields(dto.body_type, VehicleBodyTypesDbTableModel, BODY_TYPE_ATTRIBUTE)
        vehicle.loading_types = self._map_list_fields(dto.loading_type, VehicleLoadingTypesDbTableModel, LOADING_TYPE_ATTRIBUTE)
        vehicle.additional_options = self._map_list_fields(dto.additional_option, VehicleAdditionalOptionsDbTableModel, ADDITIONAL_OPTIONS_ATTRIBUTE)

        response = ReadVehicleDTO(
            id=None,
            vehicle_type=vehicle.vehicle_type,
            payload=vehicle.payload,
            pallet_capacity=vehicle.pallet_capacity,
            mark=vehicle.mark,
            model=vehicle.model,
            year=vehicle.year,
            trailer=vehicle.trailer,
            trailer_year=vehicle.trailer_year,
            trailer_type=vehicle.trailer_type,
            bitemp=vehicle.bitemp,
            euro_class=vehicle.euro_class,
            body_type=[bt.body_type for bt in vehicle.body_types],
            loading_type=[lt.loading_type for lt in vehicle.loading_types],
            additional_option=[
                ao.additional_option for ao in vehicle.additional_options
            ],
        )

        await self.repo.add(vehicle)

        response.id = vehicle.id
        return response
    
    def _map_list_fields(self, 
                         values: Iterable[str], 
                         model: Type[T], 
                         attribute_name: str) -> list[T]:
        if not values:
            return []
        return [model(**{attribute_name: value}) for value in values]