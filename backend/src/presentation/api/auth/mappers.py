from src.domain.user.dtos import UserAuthInputDto
from src.presentation.api.auth.schemas import TokenOutSchema, UserAuthSchema


class AuthUserApiMapper:
    @staticmethod
    def user_auth_schema_to_dto(schema: UserAuthSchema) -> UserAuthInputDto:
        return UserAuthInputDto(**schema.__dict__)

    @staticmethod
    def dict_to_schema(dict_: dict) -> TokenOutSchema:
        return TokenOutSchema(**dict_)
