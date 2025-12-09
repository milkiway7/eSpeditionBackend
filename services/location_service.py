from pydantic import BaseModel
from uuid import UUID

LOACTIONS = {
    "e823c5c7-dfe9-49ad-a1d4-ff5fc4ed5bf4":{
        "latitude": -34.6037, 
        "longitude": 21.0122
    },
    "772f5937-35e7-45ba-adf2-4862be8c72ac":{
        "latitude": 50.0647, 
        "longitude": -19.9450
    },
    "53a58009-13d2-496e-b573-b6d4fc87f609":{
        "latitude": 51.1079, 
        "longitude": 17.0385
    }
}

class Location(BaseModel):
    user_id: UUID
    latitude: float
    longitude: float

def set_location(location: Location):
    LOACTIONS[location.user_id] = {
        "latitude": location.latitude, 
        "longitude": location.longitude
        }
    return {"status":"ok"}

def get_location(user_id):
    return LOACTIONS.get(user_id,{"error": f"user not found: {user_id}"})