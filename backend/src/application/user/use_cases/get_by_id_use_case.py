from src.application.base_exception import EntityNotFoundError
from src.application.exception_decorator import handle_db_errors
from src.application.user.irepo import IUserRepository
from src.base_exceptions import ErrorDetails
from src.domain.user.dtos import UserOutputDto
from src.domain.user.mappers import UserDomainMapper


class UserGetByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    @handle_db_errors
    async def execute(self, user_id: str) -> UserOutputDto | None:
        user_entity = await self.user_repo.get_by_id(user_id)

        if user_entity is None:
            raise EntityNotFoundError.for_entity(
                entity_name="user", identifier="id", details=ErrorDetails(value=user_id)
            )

        return UserDomainMapper.entity_to_output_dto(user_entity) if user_entity else None
