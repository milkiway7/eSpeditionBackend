from DataBase.Repositories.base_repository import BaseRepository
from DataBase.TableModels.UserActivationTokensDbTableModel import UserActivationTokensDbTableModel

class ActivationUserRepository(BaseRepository[UserActivationTokensDbTableModel]):
    def __init__(self, session):
        super().__init__(session, UserActivationTokensDbTableModel)

    async def get_by_token(self, activation_token:str) -> str:
        activations_list = await self.filter(activation_token=activation_token)
        if not activations_list:
            return None
        return activations_list[0]

        