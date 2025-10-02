from typing import Any, TypeVar

T = TypeVar("T")


class ValidatedField(T):
    """
    Дескриптор для валидации и хранения значений атрибутов объекта с проверками типа,
    значений на `None`, длины строки (если применимо) и других пользовательских ограничений.

    Аргументы:
        expected_type (type): Ожидаемый тип значения для поля (например, str, int, и т. д.).
        nullable (bool): Флаг, разрешающий значение None для поля (по умолчанию False).

    Методы:
        __set_name__(self, owner, name):
            Автоматически определяет имя поля при создании класса.

        __get__(self, instance, owner):
            Возвращает значение поля из экземпляра объекта, если оно установлено.

        __set__(self, instance, value):
            Устанавливает значение поля для объекта после проверки на допустимость (тип, None).
    """

    def __init__(self, expected_type: type, nullable: bool = False):
        self.expected_type = expected_type
        self.nullable = nullable
        self.field_name = None  # Будет установлено в __set_name__
        self.private_name = None  # Будет установлено в __set_name__

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Автоматически вызывается при создании класса-владельца.
        Устанавливает имя поля и генерирует имя для приватного атрибута.
        """
        self.field_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> T | None:
        if instance is None:
            return self  # type: ignore

        if not hasattr(instance, self.private_name) and not self.nullable:
            raise AttributeError(f"Поле '{self.field_name}' еще не инициализировано.")

        return getattr(instance, self.private_name, None)

    def __set__(self, instance: Any, value: T | None) -> None:
        if value is None and not self.nullable:
            raise ValueError(f"Поле '{self.field_name}' не может быть None.")

        if value is not None and not isinstance(value, self.expected_type):
            raise TypeError(
                f"Поле '{self.field_name}' должно быть типа {self.expected_type.__name__}, "
                f"получено: {type(value).__name__}"
            )

        setattr(instance, self.private_name, value)
