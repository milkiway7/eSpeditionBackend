from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from DataBase.Repositories.base_repository import BaseRepository
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

class CompanyEmployeesRepository(BaseRepository[CompanyEmployeesDbTableModel]):
    def __init__(self, session):
        super().__init__(session, CompanyEmployeesDbTableModel)

    async def create_company_employee_link(self, new_link: CompanyEmployeesDbTableModel) -> CompanyEmployeesDbTableModel:
        try:
            self.session.add(new_link)
            return new_link
        except IntegrityError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise
    