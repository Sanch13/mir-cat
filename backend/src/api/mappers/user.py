from src.api.schemas.user import UserResponseSchema, UserCreateSchema
from src.data_access.models import UserModel
from src.domain.user.dtos import UserOutputDto, UserInputDto


class UserApiMapper:

    @staticmethod
    def dto_to_schema(dto: UserOutputDto) -> UserResponseSchema:
        return UserResponseSchema(
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            is_superuser=dto.is_superuser,
            is_active=dto.is_active,
            created_at= dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def schema_to_dto(schema: UserCreateSchema) -> UserInputDto:
        return UserInputDto(**schema.__dict__)