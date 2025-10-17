from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserAuthInputDto
from src.domain.user.entity import UserEntity
from src.domain.user.interfaces import IPasswordHasher


class AuthenticateUserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
    ):
        self.user_repo = user_repo
        self.hasher = hasher

    async def authenticate_user(self, dto: UserAuthInputDto) -> None | UserEntity:
        user_entity = await self.user_repo.get_by_email(email=dto.email)

        if not user_entity or not self.hasher.verify(
            plain=dto.password, hashed=user_entity.password.value
        ):
            return None
        return user_entity
