from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from Helpers.mapper import UserMapper
from Exceptions.domain_exceptions import EntityNotFoundError, EntityAlreadyExistsError
from sqlalchemy.exc import IntegrityError

class UserRepository(BaseRepository[UserDbTableModel]):
    def __init__(self, session):
        super().__init__(session, UserDbTableModel)
    
    async def get_by_id(self, id: int):
        user = await self.filter(id=id)
        if not user:
            raise EntityNotFoundError("User",id)
        return UserMapper.read_model_to_dto(user[0])
    
    async def get_by_email(self, email: str):
        user = await self.filter(email=email)
        if not user:
            raise EntityNotFoundError("User",email)
        return UserMapper.read_model_to_dto(user[0])
    
    async def add_user(self, new_user: UserDbTableModel):
        try:
            created_user = await self.add(new_user)
            return UserMapper.read_model_to_dto(created_user)
        except IntegrityError as e:
            raise EntityAlreadyExistsError("User", "email", new_user.email)