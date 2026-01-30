from DataBase.Repositories.user_repository import UserRepository
from Enums.user_roles import UserRoles
from Exceptions.domain_exceptions import ForbiddenError
from Routes.User.user_dto import DtoAddByAdmin, DtoActivateUser
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from DataBase.TableModels.UserActivationTokensDbTableModel import UserActivationTokensDbTableModel
from Services.password_encryption import hash_password
from datetime import datetime, timezone, timedelta
from Enums.user_activation_stauts import UserActivationStatus
from DataBase.Repositories.user_activation_token_repository import ActivationUserRepository
from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from datetime import datetime, timezone
from Services.authentication_service import AuthenticationService, UserJWTData
from DataBase.Repositories.companies_repository import CompaniesRepository

ACCESS_TOKEN_EXPIRATION_TIME = 24

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository= repository

    async def generate_activation_token(self, 
                                        dto: DtoAddByAdmin, 
                                        admin_user: dict, 
                                        session: AsyncSession) -> str:
        if admin_user["user_role"] == UserRoles.CARRIER_ADMIN.value:
            if dto.user_role not in [UserRoles.CARRIER_ADMIN.value,
                                     UserRoles.CARRIER_SPEDITOR.value,
                                     UserRoles.CARRIER_DRIVER.value]:
                raise ForbiddenError("Forbidden action. As SHIPPER_ADMIN availables roles to add are: CARRIER_ADMIN, CARRIER_SPEDITOR, CARRIER_DRIVER.")
            activation_token = await self.create_and_store_activation_token(dto, admin_user, session)
            return activation_token
        elif admin_user["user_role"] == UserRoles.SHIPPER_ADMIN.value:
            if dto.user_role not in [UserRoles.SHIPPER_ADMIN.value,
                                     UserRoles.SHIPPER_EMPLOYEE.value]:
                raise ForbiddenError("Forbidden action. As SHIPPER_ADMIN availables roles to add are: SHIPPER_ADMIN, SHIPPER_EMPLOYEE.")
            # stwórz UUID do weryfikacji
            activation_token = await self.create_and_store_activation_token(dto, admin_user, session)
            return activation_token
        else:
            raise ForbiddenError("Forbidden action. To add user ADMIN role is required.")  
        
    async def create_and_store_activation_token(self, dto: DtoAddByAdmin, 
                                                admin_user: dict, 
                                                session: AsyncSession) -> str:
        user_exsist = await self.repository.get_by_email(dto.email)

        if user_exsist:
            user_to_activate = user_exsist
        else:
            user_to_activate = UserDbTableModel(
                email=dto.email,
                is_active = False,
                user_role = dto.user_role,
                password = None,
                name=dto.name,
                surname=dto.surname,
                phone_number=dto.phone_number
            )
            await session.flush()

        activation_token = uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRATION_TIME)
        user_to_activate.user_activation_link.append(
                UserActivationTokensDbTableModel(
                company_id = admin_user["company_id"],
                activation_token = str(activation_token),
                expires_at = expires_at,
                used_at = None,
                status = UserActivationStatus.PENDING.value
            )
        )

        await self.repository.add(user_to_activate)
        return activation_token

    async def activate_user(self, dto: DtoActivateUser, 
                            activation_token_repository: 
                            ActivationUserRepository, 
                            session: AsyncSession):
        async with session.begin():
            activation = await activation_token_repository.get_by_token(dto.activation_token)
            if not activation:
                raise ForbiddenError("User does not exist in registrations table.")

            if activation.status != UserActivationStatus.PENDING:
                raise ForbiddenError("To activate activation status should be PENDING.")

            if activation.expires_at < datetime.now(timezone.utc):
                raise ForbiddenError("Activation link expired.")

            user = activation.user

            if user.is_active != False:
                raise ForbiddenError("User status should be inactive.")

            user.password = hash_password(dto.password)
            user.name = dto.name
            user.surname = dto.surname
            user.phone_number = dto.phone_number
            user.is_active = True
            user.company_employee_links.append(
                CompanyEmployeesDbTableModel(
                    company_id=activation.company_id
                )
            )

            activation.status = UserActivationStatus.USED.value
            activation.used_at = datetime.now(timezone.utc)
            await session.flush()

            company_repository = CompaniesRepository(session)
            company = await company_repository.get_by_id(activation.company_id)

            authentication_service = AuthenticationService()
            jwt_token = authentication_service.authenticate_after_registration(UserJWTData(
                sub=str(user.id),
                email=user.email,
                company_type= company.company_type,
                user_role=user.user_role,
                company_id=company.id,
                iat=int(datetime.now(timezone.utc).timestamp())
            ))
            return jwt_token



