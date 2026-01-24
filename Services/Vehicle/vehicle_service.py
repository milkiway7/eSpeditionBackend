from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel
from DataBase.TableModels.Vehicles.VehicleBodyTypesDbTableModel import VehicleBodyTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleLoadingTypesDbTableModel import VehicleLoadingTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleAdditionalOptionsDbTableModel import VehicleAdditionalOptionsDbTableModel
from DataBase.Repositories.vehicle_repository import VehicleRepository
from typing import TypeVar, Type, Iterable, List
from Exceptions.domain_exceptions import UnauthorizedError
from Routes.Vehicles.vehicle_dto import ReadVehicleDTO, CreateVehicleDTO, UpdateVehicleDTO
from Exceptions.domain_exceptions import UnauthorizedError, EntityNotFoundError
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
    
    async def get_vehicle(self, user: dict, vehicle_id: int) -> ReadVehicleDTO:
        if user["company_type"] != "CARRIER":
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have CARRIER account type.")
        if user["user_role"] not in [UserRoles.CARRIER_ADMIN.value, UserRoles.CARRIER_SPEDITOR.value]:
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have SPEDITOR or ADMIN role.")
        
        vehicle = await self.repo.get_by_id(vehicle_id)
        
        if not vehicle:
            raise EntityNotFoundError("Vehicle", vehicle_id)
        
        response = ReadVehicleDTO(
            id=vehicle.id,
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

        return response

    async def company_vehicles(self, user: dict) -> list[ReadVehicleDTO]:
        if user["company_type"] != "CARRIER":
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have CARRIER account type.")
        if user["user_role"] not in [UserRoles.CARRIER_ADMIN.value, UserRoles.CARRIER_SPEDITOR.value]:
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have SPEDITOR or ADMIN role.")
        
        vehicles = await self.repo.get_company_vehicles(user["company_id"])

        response = []

        for vehicle in vehicles:
            response.append(
                        ReadVehicleDTO(
                    id=vehicle.id,
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
            )

        return response

    async def update_vehicle(self,user: dict, vehicle_id: int, dto: UpdateVehicleDTO) -> ReadVehicleDTO:
        if user["company_type"] != "CARRIER":
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have CARRIER account type.")
        if user["user_role"] not in [UserRoles.CARRIER_ADMIN.value, UserRoles.CARRIER_SPEDITOR.value]:
            raise UnauthorizedError("Unauthorized access. To view a vehicle, user must have SPEDITOR or ADMIN role.")
        
        vehicle_to_update = await self.repo.get_by_id(vehicle_id)

        if not vehicle_to_update:
            raise EntityNotFoundError("Vehicle", vehicle_id)
        
        vehicle_to_update.vehicle_type = dto.vehicle_type
        vehicle_to_update.payload = dto.payload
        vehicle_to_update.pallet_capacity = dto.pallet_capacity
        vehicle_to_update.mark = dto.mark
        vehicle_to_update.model = dto.model
        vehicle_to_update.year = dto.year
        vehicle_to_update.trailer = dto.trailer
        vehicle_to_update.trailer_year = dto.trailer_year
        vehicle_to_update.trailer_type = dto.trailer_type
        vehicle_to_update.bitemp = dto.bitemp
        vehicle_to_update.euro_class = dto.euro_class

        # Relations (replace)
        vehicle_to_update.body_types.clear()
        vehicle_to_update.body_types.extend(
            self._map_list_fields(dto.body_type, VehicleBodyTypesDbTableModel,BODY_TYPE_ATTRIBUTE)
        )    

        vehicle_to_update.loading_types.clear()
        vehicle_to_update.loading_types.extend(
            self._map_list_fields(dto.loading_type, VehicleLoadingTypesDbTableModel,LOADING_TYPE_ATTRIBUTE)
        )

        vehicle_to_update.additional_options.clear()
        vehicle_to_update.additional_options.extend(
            self._map_list_fields(dto.additional_option, VehicleAdditionalOptionsDbTableModel,ADDITIONAL_OPTIONS_ATTRIBUTE)
        )

        updated_vehicle = await self.repo.update_vehicle(vehicle_to_update)

        response = ReadVehicleDTO(
            id=updated_vehicle.id,
            vehicle_type=updated_vehicle.vehicle_type,
            payload=updated_vehicle.payload,
            pallet_capacity=updated_vehicle.pallet_capacity,
            mark=updated_vehicle.mark,
            model=updated_vehicle.model,
            year=updated_vehicle.year,
            trailer=updated_vehicle.trailer,
            trailer_year=updated_vehicle.trailer_year,
            trailer_type=updated_vehicle.trailer_type,
            bitemp=updated_vehicle.bitemp,
            euro_class=updated_vehicle.euro_class,
            body_type=[bt.body_type for bt in updated_vehicle.body_types],
            loading_type=[lt.loading_type for lt in updated_vehicle.loading_types],
            additional_option=[
                ao.additional_option for ao in updated_vehicle.additional_options
            ],
        )
        
        return response
    
    def _map_list_fields(self, 
                         values: Iterable[str], 
                         model: Type[T], 
                         attribute_name: str) -> list[T]:
        if not values:
            return []
        return [model(**{attribute_name: value}) for value in values]