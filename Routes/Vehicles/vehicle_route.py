from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository
from Dependencies.authorize_user import authorize_user
from Services.Vehicle.vehicle_service import VehicleService

router = APIRouter()

@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.create_vehicle(vehicle, user)
    return {"message": "Vehicle added successfully", "vehicle": vehicle_data}