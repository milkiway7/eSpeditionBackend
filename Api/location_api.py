from fastapi import APIRouter

# router = APIRouter(prefix="/location", tags=["Location"])
router = APIRouter(prefix="/location")

@router.get("/get")
def get_location():
    return {"msg":"get loc"}

@router.put("/send")
def send_location():
    return {"msg":"send loc"}