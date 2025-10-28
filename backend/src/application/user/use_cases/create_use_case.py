from src.application.base_exception import DuplicateEntityError
from src.application.exception_decorator import handle_db_errors
from src.application.interfaces import IEmailNotificationService
from src.application.user.irepo import IUserRepository
from src.base_exceptions import ErrorDetails
from src.domain.user import PasswordHashVo
from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.interfaces import IPasswordHasher
from src.domain.user.mappers import UserDomainMapper


class UserCreateUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
        email_notification_service: IEmailNotificationService,
    ):
        self.user_repo = user_repo
        self.hasher = hasher
        self.email_notification_service = email_notification_service

    @handle_db_errors
    async def execute(self, dto: UserInputDto) -> UserOutputDto:
        if await self.user_repo.email_exists(dto.email):
            raise DuplicateEntityError.for_entity(
                entity_name="User",
                identifier="email",
                details=ErrorDetails(value=dto.email, operation="UserCreateUseCase"),
            )

        password_vo = PasswordHashVo.from_plain(plain=dto.password, hasher=self.hasher)
        user_entity = UserDomainMapper.input_dto_to_entity(dto=dto, password_vo=password_vo)

        await self.user_repo.save(user_entity)

        # data = user_entity.email.value
        # # TODO: обсудить! будем отправлять на email приветствие? или пока taskiq выкл
        # await self.email_notification_service.send_email(
        #     to_email="korneva.ol.lv@gmail.com",
        #     data=data,
        # )

        return UserDomainMapper.entity_to_output_dto(user_entity)
