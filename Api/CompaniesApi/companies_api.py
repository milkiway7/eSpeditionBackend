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

@router.get("/companies/get_by_id/{company_id}")
async def get_company_by_id(company_id: int, session: AsyncSession = Depends(get_session)):
    repo = CompaniesRepository(session)
    company = await repo.get_by_id(company_id)
    return {"Company:": CompaniesMapper.read_model_to_dto(company)}

@router.get("/companies/get_by_name/{company_name}")
async def get_company_by_name(company_name: str, session: AsyncSession = Depends(get_session)):
    repo = CompaniesRepository(session)
    company = await repo.get_by_company_name(company_name)
    return {"Company:": CompaniesMapper.read_model_to_dto(company[0])}