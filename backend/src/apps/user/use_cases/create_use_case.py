from uuid import UUID

from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserInputDto
from src.domain.user.mappers import UserDomainMapper


class UserCreateUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    # TODO: добавить обработку ошибок
    async def execute(self, dto: UserInputDto) -> UUID:
        user = UserDomainMapper.input_dto_to_entity(dto)
        await self.user_repo.save(user)
        return user.id.value
