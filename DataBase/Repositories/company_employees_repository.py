from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from DataBase.Repositories.base_repository import BaseRepository

class CompanyEmployeesRepository(BaseRepository[CompanyEmployeesDbTableModel]):
    def __init__(self, session):
        super().__init__(session, CompanyEmployeesDbTableModel)

    async def create_company_employee_link(self, new_link: CompanyEmployeesDbTableModel) -> CompanyEmployeesDbTableModel:
        self.session.add(new_link)
        return new_link
    