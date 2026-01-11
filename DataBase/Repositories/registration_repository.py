from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from DataBase.Repositories.base_repository import BaseRepository
from sqlalchemy.exc import IntegrityError
from Exceptions.domain_exceptions import EntityAlreadyExistsError

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