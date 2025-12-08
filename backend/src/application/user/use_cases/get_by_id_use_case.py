from uuid import UUID

import structlog

from src.application.base_exception import EntityNotFoundError
from src.application.exception_decorator import handle_db_errors
from src.application.user.irepo import IUserRepository
from src.base_exceptions import ErrorDetails
from src.core.tracing import traced
from src.domain.user.dtos import UserOutputDto
from src.domain.user.mappers import UserDomainMapper

logger = structlog.get_logger()


class UserGetByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    @handle_db_errors
    @traced(name="UserGetByIdUseCase.execute")
    async def execute(self, user_id: UUID) -> UserOutputDto | None:
        log = logger.bind(action="get_user_by_id")
        log.info("usecase_get_by_id_started")
        user_entity = await self.user_repo.get_by_id(user_id)

        if user_entity is None:
            log.warning("user not found", user_id=str(user_id))
            raise EntityNotFoundError.for_entity(
                entity_name="user", identifier="id", details=ErrorDetails(value=str(user_id))
            )
        log.info("usecase_get_by_id_finished_success", user_id=str(user_id))
        return UserDomainMapper.entity_to_output_dto(user_entity) if user_entity else None
