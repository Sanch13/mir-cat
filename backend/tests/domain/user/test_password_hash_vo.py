import pytest
from unittest.mock import Mock, create_autospec

from src.domain.user.value_objects import (
    MAX_PASSWORD_LENGTH,
    PasswordHashVo
)
from src.shared.exceptions import InvalidTypeError
from src.domain.user.exeptions import (
    PasswordInvalidCharactersError,
    PasswordTooLongError,
    PasswordTooShortError,
    PasswordInvalidLowercaseError,
    PasswordInvalidUppercaseError,
    PasswordInvalidDigitError,
)


@pytest.fixture
def mock_hasher():
    """Фикстура для мока IPasswordHasher"""
    hasher = create_autospec('IPasswordHasher')
    hasher.hash = Mock(return_value="hashed_password_123")
    hasher.verify = Mock(return_value=True)
    return hasher


@pytest.fixture
def valid_password():
    """Валидный пароль удовлетворяющий всем требованиям"""
    return "ValidPass123"


class TestPasswordHashVo:
    """Тесты для Value Object PasswordHashVo"""

    # Тесты для from_hash
    def test_from_hash_valid(self):
        """Тест создания VO из хеша"""
        hash_str = "some_hashed_value"
        vo = PasswordHashVo.from_hash(hash_str)
        assert vo.value == hash_str
        assert vo.hash == hash_str

    def test_from_hash_empty_string(self):
        """Тест создания VO из пустой строки"""
        with pytest.raises(ValueError, match="hash_str must be non-empty string"):
            PasswordHashVo.from_hash("")

    def test_from_plain_valid(self, mock_hasher, valid_password):
        """Тест создания VO из валидного пароля"""
        vo = PasswordHashVo.from_plain(valid_password, mock_hasher)
        assert vo.value == "hashed_password_123"
        mock_hasher.hash.assert_called_once_with(valid_password)

    def test_verify_success(self, mock_hasher, valid_password):
        """Тест успешной проверки пароля"""
        vo = PasswordHashVo.from_hash("some_hash")
        result = vo.verify(valid_password, mock_hasher)

        assert result is True
        mock_hasher.verify.assert_called_once_with(valid_password, "some_hash")

    def test_password_with_all_special_chars(self, mock_hasher):
        """Тест пароля со всеми допустимыми специальными символами"""
        special_chars = "!@#$%^&*(),.?\":{}|<>_-+="
        password = f"Valid1{special_chars}"
        vo = PasswordHashVo.from_plain(password, mock_hasher)
        assert vo.value == "hashed_password_123"

    def test_immutability(self):
        """Тест что VO иммутабельный"""
        vo = PasswordHashVo.from_hash("test_hash")

        # Попытка изменить атрибут должна вызвать ошибку
        with pytest.raises(Exception):
            vo.value = "new_value"


# Параметризованные тесты для разных валидных паролей
@pytest.mark.parametrize(
    "valid_password",
    [
        "ValidPass123!",
        "Vaso13",
        "v" * (MAX_PASSWORD_LENGTH - 2) + "V1",
        "ANOTHERpass456",
    ])
def test_various_valid_passwords(valid_password, mock_hasher):
    """Тест различных валидных паролей"""
    vo = PasswordHashVo.from_plain(valid_password, mock_hasher)
    assert vo.value == "hashed_password_123"


# Параметризованные тесты для невалидных паролей
@pytest.mark.parametrize(
    "invalid_password, expected_exception",
    [
        ("Ab1!c", PasswordTooShortError),  # слишком короткий
        ("            ", PasswordTooShortError),  # пробелы
        ("A" * MAX_PASSWORD_LENGTH + "b1!", PasswordTooLongError),  # слишком длинный
        ("VALID123!", PasswordInvalidLowercaseError),  # нет строчных
        ("valid123!", PasswordInvalidUppercaseError),  # нет заглавных
        ("ValidPass!", PasswordInvalidDigitError),  # нет цифр
        ("Valid123привет", PasswordInvalidCharactersError),  # кириллица нельзя
        ("z   R1", PasswordInvalidCharactersError),  # пробелы нельзя
        (123, InvalidTypeError),  # не строка
        (None, InvalidTypeError),  # не строка
    ])
def test_various_invalid_passwords(invalid_password, expected_exception, mock_hasher):
    """Тест различных невалидных паролей"""
    with pytest.raises(expected_exception):
        PasswordHashVo.from_plain(invalid_password, mock_hasher)
