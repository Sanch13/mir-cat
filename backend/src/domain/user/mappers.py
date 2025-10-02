from uuid import UUID

from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.entity import UserEntity
from src.domain.user.value_objects import (
    UserEmailVo,
    UserPasswordVo,
    UserFirstNameVo,
    UserLastNameVo
)


class UserDomainMapper:

    @staticmethod
    def input_dto_to_entity(dto: UserInputDto) -> UserEntity:
        return UserEntity(
            email = UserEmailVo(dto.email),
            password = UserPasswordVo(dto.password),
            first_name = UserFirstNameVo(dto.first_name) if dto.first_name else None,
            last_name = UserLastNameVo(dto.last_name) if dto.last_name else None,
            is_superuser = dto.is_superuser,
            is_active = dto.is_active
        )

    @staticmethod
    def entity_to_output_dto(entity: UserEntity) -> UserOutputDto:
        return UserOutputDto(
            id = entity.id.value,
            email = entity.email.value,
            password = entity.password.value,
            created_at = entity.created_at.value if entity.created_at else None, # в какой момент устанавливаем
            updated_at = entity.updated_at.value if entity.updated_at else None, # в какой момент устанавливаем
            first_name = entity.first_name.value if entity.first_name else None,
            last_name = entity.last_name.value if entity.last_name else None,
            is_superuser = entity.is_superuser,
            is_active = entity.is_active
        )



