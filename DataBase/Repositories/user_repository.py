from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from Helpers.mapper import UserMapper

class UserRepository(BaseRepository[UserDbTableModel]):
    def __init__(self, session):
        super().__init__(session, UserDbTableModel)

    async def get_by_email(self, email: str):
        users = await self.filter(email=email)
        return users[0] if users else None
    
    async def get_by_id(self, id: int):
        users = await self.filter(id=id)
        return users[0] if users else None
    
    async def add_user(self, new_user: UserDbTableModel):
        created_user = await self.add(new_user)
        return UserMapper.read_model_to_dto(created_user)

    
    
