from src.apps.user.irepo import IUserRepository
from src.domain.user import PasswordHashVo
from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.interfaces import IPasswordHasher
from src.domain.user.mappers import UserDomainMapper


class UserCreateUseCase:
    def __init__(self, user_repo: IUserRepository, hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    # TODO: добавить обработку ошибок
    async def execute(self, dto: UserInputDto) -> UserOutputDto:
        password_vo = PasswordHashVo.from_plain(plain=dto.password, hasher=self.hasher)
        user_entity = UserDomainMapper.input_dto_to_entity(dto=dto, password_vo=password_vo)
        await self.user_repo.save(user_entity)
        return UserDomainMapper.entity_to_output_dto(user_entity)
