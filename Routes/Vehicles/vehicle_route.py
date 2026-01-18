from fastapi import APIRouter, Depends
from dependencies import get_session
from .vehicle_dto import CreateVehicleDTO

router = APIRouter()

# Add authorization 
@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session)):

    return {"message": "Vehicle added successfully", "vehicle": vehicle}