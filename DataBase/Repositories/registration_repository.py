from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from DataBase.Repositories.base_repository import BaseRepository
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from sqlalchemy import select
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from uuid import UUID

class RegistrationsRepository(BaseRepository[RegistrationsDbTableModel]):
    def __init__(self, session):
        super().__init__(session, RegistrationsDbTableModel)

    async def start_registration(self, new_registration: RegistrationsDbTableModel) -> RegistrationsDbTableModel:
        try:
            new_registration = await self.add(new_registration)
            return new_registration
        except IntegrityError as e:
            msg = str(e.orig)
            if "uq_registration_registration_id" in msg:
                raise EntityAlreadyExistsError("Registration", "registration_id", new_registration.registration_id)
            elif "uq_registration_email" in msg:
                raise EntityAlreadyExistsError("Registration", "email", new_registration.email)
            elif "uq_registration_nip" in msg:
                raise EntityAlreadyExistsError("Registration", "nip", new_registration.nip)
            elif "uq_registration_user_phone" in msg:
                raise EntityAlreadyExistsError("Registration", "user_phone", new_registration.user_phone)
            else:
                raise e
    
    async def get_by_registration_id(self, registration_id: UUID) -> RegistrationsDbTableModel:
        query = await self.session.execute(
            select(self.model).where(self.model.registration_id == registration_id)
        )
        return query.scalar_one_or_none()
    
    async def update_company_details(self, registration_to_update: RegistrationsDbTableModel, data: dict) -> RegistrationsDbTableModel:
        for key, value in data.items():
            setattr(registration_to_update, key, value)
        await self._commit()
        await self.session.refresh(registration_to_update)
        return registration_to_update

    async def final_registration_update(self, registration_to_update: RegistrationsDbTableModel, data: dict) -> RegistrationsDbTableModel:
        try:
            for key, value in data.items():
                setattr(registration_to_update, key, value)
            self.session.add(registration_to_update)
            return registration_to_update
        except IntegrityError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise