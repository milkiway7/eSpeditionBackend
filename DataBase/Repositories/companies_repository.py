from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from Exceptions.domain_exceptions import EntityNotFoundError, EntityAlreadyExistsError
from sqlalchemy.exc import IntegrityError

class CompaniesRepository(BaseRepository[CompaniesDbTableModel]):
    def __init__(self, session):
        super().__init__(session, CompaniesDbTableModel)

    async def add_company(self, new_company: CompaniesDbTableModel) -> CompaniesDbTableModel:
        try:
            created_company = await self.add(new_company)
            return created_company
        except IntegrityError as e:
            msg = str(e.orig)
            if 'uq_company_nip' in msg:
                raise EntityAlreadyExistsError("Company", "nip", new_company.nip)
            elif 'uq_company_vat_eu' in msg:
                raise EntityAlreadyExistsError("Company", "vat_eu", new_company.vat_eu)
            elif 'uq_company_name' in msg:
                raise EntityAlreadyExistsError("Company", "company_name", new_company.company_name)
    
    async def get_by_id(self, company_id: int) -> CompaniesDbTableModel:
        company = await self.get(company_id)
        if not company:
            raise EntityNotFoundError("Company", "id", company_id)
        return company
        
    async def get_by_company_name(self, company_name: str) -> CompaniesDbTableModel:
        company = await self.filter(company_name=company_name)
        if not company:
            raise EntityNotFoundError("Company", "company_name", company_name)
        return company

