from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from Api.CompaniesApi.dto_companies import DtoCreateCompany,DtoReadCompany
from datetime import datetime

class CompaniesMapper:

    @staticmethod
    def create_dto_to_model(dto: DtoCreateCompany) -> CompaniesDbTableModel:
        company = dto.model_dump()
        return CompaniesDbTableModel(
            **company,
            created_at = datetime.now()
        )
    
    @staticmethod
    def read_model_to_dto(model: CompaniesDbTableModel) -> DtoReadCompany:
        return DtoReadCompany.model_validate(model)