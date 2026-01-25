from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from .vehicle_dto import CreateVehicleDTO, UpdateVehicleDTO
from DataBase.Repositories.vehicle_repository import VehicleRepository
from Dependencies.authorize_user import authorize_user
from Services.Vehicle.vehicle_service import VehicleService

router = APIRouter()

@router.post("/vehicle/add", status_code=201)
async def add_vehicle(vehicle: CreateVehicleDTO, session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.create_vehicle(vehicle, user)
    return {"message": "Vehicle added successfully", "vehicle": vehicle_data}

@router.get("/vehicle/{vehicle_id}", status_code=200)
async def get_vehicle(vehicle_id: int, session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.get_vehicle(user, vehicle_id)
    return {"message": "Company vehicle fetched", "vehicle": vehicle_data}

@router.get("/vehicles/company", status_code=200)
async def get_company_vehicles(session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicles_data = await vehicle_service.company_vehicles(user)
    return {"message": "Company vehicles fetched", "vehicle": vehicles_data}

@router.put("/vehicle/{vehicle_id}", status_code=200)
async def update_vehicle(vehicle_id: int, vehicle_dto: UpdateVehicleDTO,session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicles_data = await vehicle_service.update_vehicle(user, vehicle_id ,vehicle_dto)
    return {"message": "Company vehicle updated", "vehicle": vehicles_data}

@router.delete("/vehicle/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id:int,session=Depends(get_session), user=Depends(authorize_user)):
    vehicle_service = VehicleService(VehicleRepository(session))
    vehicle_data = await vehicle_service.delete_vehicle(user, vehicle_id)
    return {"message": "Company vehicle deleted", "vehicle_id": vehicle_data}
