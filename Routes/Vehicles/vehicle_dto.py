from pydantic import BaseModel, Field

class CreateVehicleDTO(BaseModel):
    car_type: str = Field(min_length=2, max_length=50)
    payload:int = Field(gt=0)
    pallet_capacity:int = Field(gt=0)
    mark: str | None = Field(min_length=1, max_length=50)
    model: str | None = Field(min_length=1, max_length=50)
    year: int = Field(ge=1990, le=2100)
    trailer: bool
    trailer_year: int | None = Field(ge=1990, le=2100)
    trailer_type: str | None = Field(min_length=2, max_length=50)
    bitemp: bool
    euro_class: str = Field(min_length=2, max_length=50)
    body_type: list[str] = Field(min_items=1)
    loading_type: list[str] = Field(min_items=1)
    additional_options: list[str] | None
