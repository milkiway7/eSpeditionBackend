from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from Routes.Registration.registration_dto import RegistrationStartDTO, RegistrationReadDTO
from Enums.registration_status import RegistrationStatus
from Services.password_encryption import hash_password

class RegistrationMapper:

    @staticmethod
    def registration_start_dto_to_model(dto: RegistrationStartDTO,
                                         company_name: str) -> RegistrationsDbTableModel:
        registration = dto.model_dump()
        password = registration.get("password")
        if password is None:
            raise ValueError("Password cannot be None")
        registration["password"] = hash_password(password)

        return RegistrationsDbTableModel(
            **registration,
            registration_status=RegistrationStatus.KRS_VERIFIED,
            company_name=company_name
        )
    
    @staticmethod
    def db_model_to_dto(model: RegistrationsDbTableModel) -> RegistrationReadDTO:
        return RegistrationReadDTO(
            registration_id=model.registration_id,
            company_name=model.company_name,
            nip=model.nip
        )