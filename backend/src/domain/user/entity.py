import uuid
from datetime import UTC, datetime

from src.domain.user.value_objects import (
    UserCreatedAtVo,
    UserEmailVo,
    UserFirstNameVo,
    UserIdVo,
    UserLastNameVo,
    UserPasswordVo,
    UserUpdatedAtVo,
)
from src.shared.decriptor import ValidatedField
from src.shared.exceptions import InvalidTypeError


class UserEntity:
    email = ValidatedField(expected_type=UserEmailVo, nullable=False)
    password = ValidatedField(expected_type=UserPasswordVo, nullable=False)
    created_at = ValidatedField(expected_type=UserCreatedAtVo, nullable=True)
    updated_at = ValidatedField(expected_type=UserUpdatedAtVo, nullable=True)
    first_name = ValidatedField(expected_type=UserFirstNameVo, nullable=True)
    last_name = ValidatedField(expected_type=UserLastNameVo, nullable=True)
    is_superuser = ValidatedField(expected_type=bool, nullable=True)
    is_active = ValidatedField(expected_type=bool, nullable=True)

    def __init__(
        self,
        email: UserEmailVo,
        password: UserPasswordVo,
        created_at: UserCreatedAtVo | None = None,
        updated_at: UserUpdatedAtVo | None = None,
        first_name: UserFirstNameVo | None = None,
        last_name: UserLastNameVo | None = None,
        is_superuser: bool = False,
        is_active: bool = True,
        id_: UserIdVo | None = None,
    ) -> None:
        self.email = email
        self.password = password
        self.created_at = created_at or UserCreatedAtVo(datetime.now(UTC))
        self.updated_at = updated_at or UserUpdatedAtVo(self.created_at.value)
        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser
        self.is_active = is_active
        self._id = id_ or UserIdVo(uuid.uuid4())

    @property
    def id(self) -> UserIdVo:
        return self._id

    @id.setter
    def id(self, value: UserIdVo) -> None:
        """Сеттер для ID"""
        if self._id is not None:
            raise AttributeError("Item ID уже установлен.")
        if not isinstance(value, UserIdVo):
            raise InvalidTypeError(
                message_to_extend={
                    "expected_type": UserIdVo,
                    "attr_name": "value of UserIdVo",
                    "actual_type": type(value).__name__,
                    "value": value,
                }
            )
        self._id = value

    # TODO: проверить необходимость
    def __repr__(self) -> str:
        if self.id is not None:
            return f"{self.__class__.__name__} (ID: {self.id.value}, email: {self.email.value}) "
        return f"{self.__class__.__name__} (no ID, email: {self.email.value})"
