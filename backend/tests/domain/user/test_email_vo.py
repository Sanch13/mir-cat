import pytest

from src.domain.user.exeptions import EmailInvalidFormatError, EmailInvalidCharactersError
from src.domain.user.value_objects import UserEmailVo

VALID_EMAIL = 'test@domain.com'
MISS_COMMERCIAL_AT = ['test-email', 'test-domain.com']
DOUBLE_COMMERCIAL_AT = ['@test@', 'test@@domain.com', 'test@domain@.com']
MISS_LOCAL_PART_OR_DOMAIN = ['test@', '@domain.com']
CONSECUTIVE_DOTS = ['test..@domain.com', 'test@domain..com', 'test@domain.co..m']
WRONG_SYMBOLS = [
    # Кириллические символы в локальной части
    ('Яtest@domain.com', 'Я'),
    ('тест@domain.com', 'т'),
    ('testы@domain.com', 'ы'),

    # Кириллические символы в домене
    ('test@Яdomain.com', 'Я'),
    ('test@домен.com', 'д'),
    ('test@domain.рф', 'р'),

    # Символы, запрещенные в локальной части
    ('test(@domain.com', '('),
    ('test)@domain.com', ')'),
    ('test[@domain.com', '['),
    ('test]@domain.com', ']'),
    ('test<@domain.com', '<'),
    ('test>@domain.com', '>'),
    ('test,@domain.com', ','),
    ('test;@domain.com', ';'),
    ('test:@domain.com', ':'),
    ('test"@domain.com', '"'),
    ('test\\@domain.com', '\\'),

    # Символы, запрещенные в начале и конце локальной части
    ('!test@domain.com', '!'),
    ('test!@domain.com', '!'),
    ('#test@domain.com', '#'),
    ('test#@domain.com', '#'),
    ('$test@domain.com', '$'),
    ('test$@domain.com', '$'),
    ('test@domain%.com', '%'),
    ('%test@domain.com', '%'),
    ('test%@domain.com', '%'),
    ('%test@domain.com', '%'),
    ('&test@domain.com', '&'),
    ('*test@domain.com', '*'),
    ('+test@domain.com', '+'),
    ('=test@domain.com', '='),
    ('/test@domain.com', '/'),
    ('?test@domain.com', '?'),
    ('|test@domain.com', '|'),
    ('test%@domain.com', '%'),
    ('test&@domain.com', '&'),
    ('test*@domain.com', '*'),
    ('test+@domain.com', '+'),
    ('test=@domain.com', '='),
    ('test/@domain.com', '/'),
    ('test?@domain.com', '?'),
    ('test|@domain.com', '|'),
    ('test%@domain.com', '%'),
    ('test&@domain.com', '&'),
    ('test*@domain.com', '*'),
    ('test+@domain.com', '+'),
    ('test=@domain.com', '='),
    ('test/@domain.com', '/'),
    ('test?@domain.com', '?'),
    ('test|@domain.com', '|'),

    # Символы, запрещенные в доменной части
    ('test@domain!.com', '!'),
    ('test@domain#.com', '#'),
    ('test@domain$.com', '$'),
    ('test@domain%.com', '%'),
    ('test@domain&.com', '&'),
    ('test@domain*.com', '*'),
    ('test@domain+.com', '+'),
    ('test@domain=.com', '='),
    ('test@domain/.com', '/'),
    ('test@domain?.com', '?'),
    ('test@domain|.com', '|'),

    ('test@d(omain.com', '('),
    ('test@d)omain.com', ')'),
    ('test@[domain.com', '['),
    ('test@]domain.com', ']'),
    ('test@<domain.com', '<'),
    ('test@>domain.com', '>'),
    ('test@,domain.com', ','),
    ('test@;domain.com', ';'),
    ('test@:domain.com', ':'),
    ('test@"domain.com', '"'),
    ('test@d\\omain.com', '\\'),

    # Пробелы и управляющие символы
    ('test @domain.com', ' '),
    ('test@ domain.com', ' '),
    ('test\t@domain.com', '\t'),
    ('test\n@domain.com', '\n'),
]

@pytest.mark.unit
def test_valid_email():
    assert UserEmailVo(VALID_EMAIL).value == VALID_EMAIL

@pytest.mark.unit
def test_valid_email_get_local_part():
    assert UserEmailVo(VALID_EMAIL).local_part == 'test'

@pytest.mark.unit
def test_valid_email_get_domain():
    assert UserEmailVo(VALID_EMAIL).domain == 'domain.com'

@pytest.mark.unit
@pytest.mark.parametrize("email", MISS_COMMERCIAL_AT)
def test_invalid_email_miss_commercial_at(email):
    with pytest.raises(
            EmailInvalidFormatError,
            match='email must contain @ symbol'
    ):
        UserEmailVo(email)

@pytest.mark.unit
@pytest.mark.parametrize("email", DOUBLE_COMMERCIAL_AT)
def test_invalid_email_double_commercial_at(email):
    with pytest.raises(
            EmailInvalidFormatError,
            match='email must have exactly one @ symbol'
    ):
        UserEmailVo(email)

@pytest.mark.unit
@pytest.mark.parametrize("email", MISS_LOCAL_PART_OR_DOMAIN)
def test_invalid_email_miss_local_part_or_domain(email):
    with pytest.raises(
            EmailInvalidFormatError,
            match='email must have both local part and domain'
    ):
        UserEmailVo(email)

@pytest.mark.unit
def test_invalid_email_miss_dots_into_domain():
    with pytest.raises(
            EmailInvalidFormatError,
            match='domain must contain at least one dot'
    ):
        UserEmailVo('test@domaincom')

@pytest.mark.unit
def test_invalid_email_miss_top_level_domain():
    with pytest.raises(
            EmailInvalidFormatError,
            match='domain must contain top level domain after a dot'
    ):
        UserEmailVo('test@domain.')

@pytest.mark.unit
@pytest.mark.parametrize("email,wrong_symbols", WRONG_SYMBOLS)
def test_invalid_email_wrong_symbols(email, wrong_symbols):
    with pytest.raises(
            EmailInvalidCharactersError,
            match=f'contains invalid characters'
    ) as err:
        UserEmailVo(email)

    for symb in wrong_symbols:
        assert f"'{symb}'" in str(err.value)

@pytest.mark.unit
@pytest.mark.parametrize("email", CONSECUTIVE_DOTS)
def test_invalid_email_consecutive_dots(email):
    with pytest.raises(
            EmailInvalidFormatError,
            match='email cannot contain consecutive dots'
    ):
        UserEmailVo(email)

@pytest.mark.unit
def test_invalid_email_consecutive_dots():
    with pytest.raises(
            EmailInvalidFormatError,
            match='email cannot contain consecutive dots'
    ):
        UserEmailVo('.test@domain.com')

@pytest.mark.unit
@pytest.mark.parametrize("email", ['test@-domain.com', 'test@domain.com-'])
def test_invalid_email_consecutive_dots(email):
    with pytest.raises(
            EmailInvalidFormatError,
            match='domain cannot start or end with hyphen'
    ):
        UserEmailVo(email)
