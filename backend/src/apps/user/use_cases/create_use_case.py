import uuid
from uuid import UUID

from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserInputDto
from src.domain.user.mappers import UserMapper


class UserCreateUseCase:

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, dto: UserInputDto) -> UUID:
        user_id = uuid.uuid4()
        user = UserMapper.input_dto_to_entity(dto, user_id)
        await self.user_repo.save(user)
        return user_id