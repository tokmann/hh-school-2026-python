import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


# Ниже добавил 5 тестов для проверки валидации при создании пользователя в классе User
def test_validation_id_must_be_int() -> None:
    with pytest.raises(TypeError):
        LocalUser("abc", "Ivan Ivanov", "+79990000000")


def test_validation_fullname_must_be_str() -> None:
    with pytest.raises(TypeError):
        LocalUser(1, 123, "+79990000000")


def test_validation_fullname_cannot_be_empty() -> None:
    with pytest.raises(ValueError):
        LocalUser(1, "   ", "+79990000000")


def test_validation_phone_must_be_str() -> None:
    with pytest.raises(TypeError):
        LocalUser(1, "Ivan Ivanov", 79990000000)


def test_validation_phone_cannot_be_empty() -> None:
    with pytest.raises(ValueError):
        LocalUser(1, "Ivan Ivanov", "   ")


# Так как я добавил в Switchboard новый метод с валидацией, и также добавил проверку на кол-во частей в register_call, то для этого также создал тесты
def test_register_call_with_insufficient_parts() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,John Smith"
        )


def test_register_call_with_excessive_parts() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567,extra"
        )


def test_register_call_with_whitespace_parts() -> None:
    switchboard = Switchboard()

    call = switchboard.register_call(
        "1,   Ivan Ivanov   ,+79990000000,2,  John Smith  ,+15551234567"
    )
    
    assert call.caller.fullname == "Ivan Ivanov"
    assert call.receiver.fullname == "John Smith"


def test_register_call_with_invalid_user_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(TypeError):
        switchboard.register_call(
            "abc,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
        )


def test_register_call_with_empty_name() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call(
            "1,   ,+79990000000,2,John Smith,+15551234567"
        )


def test_register_call_with_numeric_string_name() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call(
            "1,12345,+79990000000,2,John Smith,+15551234567"
        )


def test_register_call_with_invalid_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError):
        switchboard.register_call(
            "1,Ivan Ivanov,79990000000,2,John Smith,+15551234567"
        )


