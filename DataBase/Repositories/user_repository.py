from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.UserDbTableModel import UserDbTableModel

class UserRepository(BaseRepository[UserDbTableModel]):
    def __init__(self, session):
        super().__init__(session, UserDbTableModel)

    async def get_by_email(self, email: str):
        users = await self.filter(email=email)
        return users[0] if users else None
    
    async def get_by_id(self, id: int):
        users = await self.filter(id=id)
        return users[0] if users else None
    
    
