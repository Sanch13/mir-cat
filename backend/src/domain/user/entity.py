import uuid
from typing import Self

from src.domain.user.value_objects import (
    UserIdVo,
    UserEmailVo,
    UserPasswordVo,
    UserCreatedAtVo,
    UserUpdatedAtVo,
    UserFirstNameVo,
    UserLastNameVo
)
from src.shared.decriptor import ValidatedField
from src.shared.exceptions import InvalidTypeError, EntityWithoutIdHashError


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
        self.created_at = created_at
        self.updated_at = updated_at
        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser
        self.is_active = is_active
        self._id = id_

    @property
    def id(self) -> UserIdVo:
        return self._id

    @id.setter
    def id(self, value: UserIdVo) -> None:
        """Сеттер для ID"""
        if self._id is not None:
            raise AttributeError('Item ID уже установлен.')
        if not isinstance(value, UserIdVo):
            raise InvalidTypeError(message_to_extend={
                'expected_type': UserIdVo,
                'attr_name': 'value of UserIdVo',
                'actual_type': type(value).__name__,
                'value': value
            })
        self._id = value


    def __eq__(self, other: Self | object) -> bool:
        """
        Compare two entities by their ID.

        Args:
            other (Any): Another object to compare with.

        Returns:
            bool: True if both objects are entities and have the same ID,
                  False otherwise.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.id is None or other.id is None:
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            raise EntityWithoutIdHashError(message_to_extend={"entity": self.__class__.__name__})
        return hash((self.__class__, self.id))

    def __repr__(self) -> str:
        if self.id is not None:
            return f"{self.__class__.__name__} (ID: {self.id.value}, email: {self.email.value}) "
        return f"{self.__class__.__name__} (no ID, email: {self.email.value})"


uuid_u1 = UserIdVo(uuid.uuid4())
u1 = UserEntity(id_=uuid_u1, email=UserEmailVo('ghjgh@gmai.ru'), password=UserPasswordVo('knknikinini'))
u2 = UserEntity(id_=uuid_u1, email=UserEmailVo('ghjgh@gmii.ru'), password=UserPasswordVo('knknikijuoinini'))
u1.is_superuser = False
u1.first_name = UserFirstNameVo('kjknh')
print(u1.is_superuser)
print(u1.first_name.value)
print(u1==u2)




# @dataclass
# class User:
#     """ Доменная сущность User """
#     id: UserId
#
#
#     @staticmethod
#     def create(
#             email: str,
#             password: str,
#             first_name: str | None = None,
#             last_name: str | None = None,
#             is_superuser: bool = False,
#             is_active: bool = True
#     ) -> "User":
#                 return User(
#                     id=UserId(value=uuid4()),
#                     email=UserEmailVO(email),
#                     password=UserPasswordVO(password),
#                     created_at=UserCreatedAtVO(datetime.now()),
#                     updated_at=UserUpdatedAtVO(datetime.now()),
#                     first_name=UserFirstName(first_name) if first_name else None,
#                     last_name=UserLastName(last_name) if last_name else None,
#                     is_superuser=is_superuser,
#                     is_active=is_active
#                 )
#
# u = User.create(email='jj', password='jjj')
# print(u)
#