from src.domain.user.dtos import UserAuthInputDto
from src.presentation.api.auth.schemas import UserAuthSchema


class AuthUserApiMapper:
    @staticmethod
    def user_auth_schema_to_dto(schema: UserAuthSchema) -> UserAuthInputDto:
        return UserAuthInputDto(**schema.__dict__)
