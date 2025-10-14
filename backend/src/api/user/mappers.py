from src.api.user.schemas import UserAuthSchema, UserCreateSchema, UserResponseSchema
from src.domain.user.dtos import UserAuthInputDto, UserInputDto, UserOutputDto


class UserApiMapper:
    @staticmethod
    def dto_to_schema(dto: UserOutputDto) -> UserResponseSchema:
        return UserResponseSchema(
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            is_superuser=dto.is_superuser,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    @staticmethod
    def schema_to_dto(schema: UserCreateSchema) -> UserInputDto:
        return UserInputDto(**schema.__dict__)

    @staticmethod
    def user_auth_schema_to_dto(schema: UserAuthSchema) -> UserAuthInputDto:
        return UserAuthInputDto(**schema.__dict__)
