from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository
from Dependencies.authorize_user import authorize_user
from Exceptions.domain_exceptions import UnauthorizedError
from Enums.user_roles import UserRoles
from .vehicle_mapper import map_vehicle_to_dto

router = APIRouter()

@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session), user=Depends(authorize_user)):
    # Check if user is CARRIER
    if user["company_type"] != "CARRIER":
        raise UnauthorizedError("Unauthorized access. To add a vehicle, user must have CARRIER account type.")
    if user["user_role"] not in [UserRoles.SPEDITOR.value, UserRoles.ADMIN.value]:
        raise UnauthorizedError("Unauthorized access. To add a vehicle, user must have SPEDITOR or ADMIN role.")
    
    vehicle_repo = VehicleRepository(session)
    vehicle_data = await vehicle_repo.add_vehicle(vehicle, user["company_id"])
    vehicle_dto = map_vehicle_to_dto(vehicle_data)
    return {"message": "Vehicle added successfully", "vehicle": vehicle_dto}