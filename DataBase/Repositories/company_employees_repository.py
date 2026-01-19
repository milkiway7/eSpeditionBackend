from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from DataBase.Repositories.base_repository import BaseRepository
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from Exceptions.domain_exceptions import EntityNotFoundError

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
    
    async def get_by_user_id(self, user_id: int) -> CompanyEmployeesDbTableModel:
        result = await self.filter(user_id=user_id)
        if not result:
            raise EntityNotFoundError(f"Company employee link for user_id {user_id} not found")
        return result[0]
    