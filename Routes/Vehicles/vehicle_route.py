from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository

router = APIRouter()

# Add authorization 
@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session)):
    vehicle_repo = VehicleRepository(session)
    vehicle = await vehicle_repo.add_vehicle(vehicle)
    return {"message": "Vehicle added successfully", "vehicle": vehicle}