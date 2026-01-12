import httpx
import os
from datetime import datetime
from Exceptions.domain_exceptions import EntityNotFoundError, ExternalServiceUnavailable
from Exceptions.registration_exceptions import KrsInactiveError
from pydantic import BaseModel

COMPANY_ACTIVE_STATUS = "Czynny"

class CompanyKrsVerificationDTO(BaseModel):
    company_name: str
    nip: str

async def verify_company_by_nip(nip: str) -> CompanyKrsVerificationDTO:
    current_date = datetime.now().strftime("%Y-%m-%d")
    async with httpx.AsyncClient(
        headers={"Accept": "application/json"},
        base_url=os.getenv("KRS_VERIFICATION_URL"),
        timeout=5.0
    ) as client:
        try:
            response = await client.get(f"/api/search/nip/{nip}?date={current_date}")
        except httpx.RequestError:
            raise ExternalServiceUnavailable()
        
        if response.status_code == 404:
            raise EntityNotFoundError(entity="Company in KRS", entity_id=nip)
        
        if response.status_code >= 500:
            raise ExternalServiceUnavailable()
        
        data = response.json()

        # check status of the company in data "statusVat": "Czynny"
        if not is_company_active(data):
            raise KrsInactiveError(nip=nip)
        
        return CompanyKrsVerificationDTO(
            company_name=data.get("result", {}).get("subject", {}).get("name"),
            nip=data.get("result", {}).get("subject", {}).get("nip")
        )
    
def is_company_active(data: dict):
    return data.get("result", {}).get("subject", {}).get("statusVat") == COMPANY_ACTIVE_STATUS

