from uuid import UUID

from src.apps.base_apps_exception import EntityNotFoundError
from src.apps.exception_handler import handle_db_errors
from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserOutputDto
from src.domain.user.mappers import UserDomainMapper
from src.shared.error_codes import ErrorCode


class UserGetByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    @handle_db_errors
    async def execute(self, user_id: UUID) -> UserOutputDto | None:
        user_entity = await self.user_repo.get_by_id(user_id)
        if user_entity is None:
            raise EntityNotFoundError.for_entity(
                entity_name="user",
                identifier="id",
                value=str(user_id),
                code=ErrorCode.USER_NOT_FOUND,
            )

        return UserDomainMapper.entity_to_output_dto(user_entity) if user_entity else None
