from src.data_access.models import UserModel
from src.domain.user.entity import UserEntity
from src.domain.user.value_objects import (
    UserCreatedAtVo,
    UserEmailVo,
    UserFirstNameVo,
    UserIdVo,
    UserLastNameVo,
    UserPasswordVo,
    UserUpdatedAtVo,
)


class UserModelMapper:
    @staticmethod
    def entity_to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name.value if entity.first_name else None,
            last_name=entity.last_name.value if entity.last_name else None,
            is_superuser=entity.is_superuser,
            is_active=entity.is_active,
        )

    @staticmethod
    def model_to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id_=UserIdVo(model.id),
            email=UserEmailVo(model.email),
            password=UserPasswordVo(model.password),
            first_name=UserFirstNameVo(model.first_name) if model.first_name else None,
            last_name=UserLastNameVo(model.first_name) if model.first_name else None,
            is_superuser=model.is_superuser,
            is_active=model.is_active,
            created_at=UserCreatedAtVo(model.created_at),
            updated_at=UserUpdatedAtVo(model.updated_at),
        )
