from Api.Dto.dto_user import DtoCreateUser, DtoReadUser
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from datetime import datetime
from Helpers.password_encryption import hash_password

class UserMapper:

    @staticmethod
    def create_dto_to_model(dto: DtoCreateUser) -> UserDbTableModel:
        user = dto.model_dump()
        pwd = user.get("password")
        if pwd is None:
            raise ValueError("Password cannot be None")
        user["password"] = hash_password(str(pwd))

        return UserDbTableModel(
            **user,
            created_at = datetime.now()
        )
    
    @staticmethod
    def read_model_to_dto(model: UserDbTableModel) -> DtoReadUser:
        return DtoReadUser.model_validate(model)