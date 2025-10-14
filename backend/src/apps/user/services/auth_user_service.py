from src.apps.user.irepo import IUserRepository
from src.domain.user.dtos import UserAuthInputDto
from src.domain.user.interfaces import IPasswordHasher


class AuthenticateUserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
    ):
        self.user_repo = user_repo
        self.hasher = hasher

    async def authenticate_user(self, dto: UserAuthInputDto) -> dict:
        user_entity = await self.user_repo.get_by_email(email=dto.email)

        if not user_entity:
            return {"message": "User does not exist."}
        else:
            verify = self.hasher.verify(plain=dto.password, hashed=user_entity.password.value)
            if verify:
                return {"message": "User exist. That's good. Open door"}
            else:
                return {"message": "Password is wrong."}
