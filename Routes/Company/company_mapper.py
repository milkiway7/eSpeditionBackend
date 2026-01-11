from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from Routes.Company.company_dto import DtoCreateCompany,DtoReadCompany
from datetime import datetime

class CompaniesMapper:

    @staticmethod
    def create_dto_to_model(dto: DtoCreateCompany, company_name: str) -> CompaniesDbTableModel:
        company = dto.model_dump()
        return CompaniesDbTableModel(
            **company,
            company_name=company_name
        )
    
    @staticmethod
    def read_model_to_dto(model: CompaniesDbTableModel) -> DtoReadCompany:
        return DtoReadCompany.model_validate(model)