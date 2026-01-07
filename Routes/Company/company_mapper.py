from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from Routes.Company.dto_company import DtoCreateCompany,DtoReadCompany
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