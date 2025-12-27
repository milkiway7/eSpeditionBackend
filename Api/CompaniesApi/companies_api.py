from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Api.CompaniesApi.dto_companies import DtoCreateCompany
from dependencies import get_session
from DataBase.Repositories.companies_repository import CompaniesRepository
from Api.CompaniesApi.companies_mapper import CompaniesMapper
router = APIRouter()

@router.post("/companies/create")
async def create_company(company: DtoCreateCompany, session: AsyncSession = Depends(get_session)):
    db_company = CompaniesMapper.create_dto_to_model(company)
    repo = CompaniesRepository(session)
    created_company = await repo.add_company(db_company)
    return {"Company created:": CompaniesMapper.read_model_to_dto(created_company)}