from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel
from .vehicle_dto import ReadVehicleDTO

def map_vehicle_to_dto(vehicle: CompanyVehiclesDbTableModel) -> ReadVehicleDTO:
    return ReadVehicleDTO(
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
        additional_option=[ao.additional_option for ao in vehicle.additional_options] if vehicle.additional_options else None
    )