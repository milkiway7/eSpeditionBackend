from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from Routes.Registration.registration_dto import RegistrationStartDTO, RegistrationReadDTO
from Enums.registration_status import RegistrationStatus

class RegistrationMapper:

    @staticmethod
    def registration_start_dto_to_model(dto: RegistrationStartDTO,
                                         company_name: str) -> RegistrationsDbTableModel:
        registration = dto.model_dump()
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