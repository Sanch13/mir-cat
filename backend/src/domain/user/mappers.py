from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.entity import UserEntity
from src.domain.user.value_objects import (
    PasswordHashVo,
    UserEmailVo,
    UserFirstNameVo,
    UserLastNameVo,
)


class UserDomainMapper:
    @staticmethod
    def input_dto_to_entity(dto: UserInputDto, password_vo: PasswordHashVo) -> UserEntity:
        return UserEntity(
            email=UserEmailVo(dto.email),
            password=password_vo,
            first_name=UserFirstNameVo(dto.first_name) if dto.first_name else None,
            last_name=UserLastNameVo(dto.last_name) if dto.last_name else None,
            is_superuser=dto.is_superuser,
            is_active=dto.is_active,
        )

    # TODO ошибки с None устранить
    @staticmethod
    def entity_to_output_dto(entity: UserEntity) -> UserOutputDto:
        return UserOutputDto(
            id=entity.id.value,
            email=entity.email.value,
            created_at=entity.created_at.value,
            updated_at=entity.updated_at.value,
            first_name=entity.first_name.value if entity.first_name else None,
            last_name=entity.last_name.value if entity.last_name else None,
            is_superuser=entity.is_superuser,
            is_active=entity.is_active,
        )
