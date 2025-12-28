from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from Exceptions.domain_exceptions import EntityNotFoundError, EntityAlreadyExistsError
from sqlalchemy.exc import IntegrityError

class UserRepository(BaseRepository[UserDbTableModel]):
    def __init__(self, session):
        super().__init__(session, UserDbTableModel)
    
    async def get_by_id(self, id: int):
        user = await self.filter(id=id)
        if not user:
            raise EntityNotFoundError("User",id)
        return user[0]
    
    async def get_by_email(self, email: str):
        user = await self.filter(email=email)
        if not user:
            raise EntityNotFoundError("User",email)
        return user[0]
    
    async def add_user(self, new_user: UserDbTableModel):
        try:
            created_user = await self.add(new_user)
            return created_user
        except IntegrityError as e:
            raise EntityAlreadyExistsError("User", "email", new_user.email)
        
    async def update_user(self, id: int, data: dict):
        user = await self.update(id, data)
        if not user:
            raise EntityNotFoundError("User",id)
        return user
    
    async def delete_user(self, id: int):
        deleted_user = await self.delete(id)
        if not deleted_user:
            raise EntityNotFoundError("User",id)
        return deleted_user 
    
    
        
        