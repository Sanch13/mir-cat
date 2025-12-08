import structlog

from src.application.base_exception import DuplicateEntityError
from src.application.exception_decorator import handle_db_errors
from src.application.interfaces import IEmailNotificationService
from src.application.user.irepo import IUserRepository
from src.base_exceptions import ErrorDetails
from src.core.tracing import traced
from src.domain.user import PasswordHashVo
from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.interfaces import IPasswordHasher
from src.domain.user.mappers import UserDomainMapper

logger = structlog.get_logger()


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
    @traced(name="CreateUserUseCase.execute")
    async def execute(self, dto: UserInputDto) -> UserOutputDto:
        log = logger.bind(email=dto.email, action="user_create_usecase")
        log.info("usecase_started")
        if await self.user_repo.email_exists(dto.email):
            log.warning("registration_failed_duplicate_email")
            raise DuplicateEntityError.for_entity(
                entity_name="User",
                identifier="email",
                details=ErrorDetails(value=dto.email, operation="UserCreateUseCase"),
            )

        password_vo = PasswordHashVo.from_plain(plain=dto.password, hasher=self.hasher)
        user_entity = UserDomainMapper.input_dto_to_entity(dto=dto, password_vo=password_vo)

        await self.user_repo.save(user_entity)
        log = log.bind(user_id=str(user_entity.id.value))
        log.info("usecase_finished_success")
        return UserDomainMapper.entity_to_output_dto(user_entity)
