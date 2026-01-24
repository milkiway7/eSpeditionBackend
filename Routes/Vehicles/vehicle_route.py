from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO, UpdateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository
from Dependencies.authorize_user import authorize_user
from Services.Vehicle.vehicle_service import VehicleService

router = APIRouter()

@router.post("/vehicle/add")
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.create_vehicle(vehicle, user)
    return {"message": "Vehicle added successfully", "vehicle": vehicle_data}

@router.get("/vehicle/{vehicle_id}")
async def get_vehicle(vehicle_id: int, session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.get_vehicle(user, vehicle_id)
    return {"vehicle": vehicle_data}

@router.get("/vehicles/company")
async def get_company_vehicles(session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicles_data = await vehicle_service.company_vehicles(user)
    return {"company_vehicles": vehicles_data}

@router.put("/vehicle/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle_dto: UpdateVehicleDTO,session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicles_data = await vehicle_service.update_vehicle(user, vehicle_id ,vehicle_dto)
    return {"company_vehicles": vehicles_data}
