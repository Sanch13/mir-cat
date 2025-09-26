from uuid import UUID

from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserOutputDto
from src.domain.user.mappers import UserMapper


class UserGetByIdUseCase:

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID) -> UserOutputDto | None:
        user_entity = await self.user_repo.get_by_id(user_id)
        return UserMapper.entity_to_output_dto(user_entity) if user_entity else None