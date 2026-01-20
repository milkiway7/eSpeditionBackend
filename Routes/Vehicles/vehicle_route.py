from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository
from Dependencies.authorize_user import authorize_user
from Exceptions.domain_exceptions import UnauthorizedError
router = APIRouter()

# Add authorization 
@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session), user=Depends(authorize_user)):
    # Check if user is CARRIER
    if user["account_type"] != "CARRIER":
        raise UnauthorizedError("Unauthorized access. To add a vehicle, user must have CARRIER account type.")

    vehicle_repo = VehicleRepository(session)
    vehicle = await vehicle_repo.add_vehicle(vehicle)
    return {"message": "Vehicle added successfully", "vehicle": vehicle}