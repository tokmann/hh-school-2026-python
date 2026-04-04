from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        # Добавил счетчик чтобы get_cross_border_calls_count() работал за O(1)
        self._cross_border_calls_count: int = 0

    # Также добавил новый приватный метод для создания пользователя с валидацией данных
    def _create_user(self, user_id: int, name: str, phone: str) -> User:
        try:
            id = int(user_id)
        except ValueError:
            raise TypeError("User id must be int")
        
        if not name:
            raise ValueError("User name cannot be empty")
        
        if name.isdigit():
            raise ValueError("User name cannot be numeric")

        if not phone.startswith('+'):
            raise ValueError("User phone must start with '+'")

        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(id, name, phone)
        else:
            return ForeignUser(id, name, phone)

    def register_call(self, raw_call: str) -> ActiveCall:
        parts = raw_call.split(',')

        if len(parts) != 6:
            raise ValueError(f"Expected 6 parts in raw_call, got {len(parts)}")
    
        caller = self._create_user(parts[0].strip(), parts[1].strip(), parts[2].strip())
        receiver = self._create_user(parts[3].strip(), parts[4].strip(), parts[5].strip())

        call = ActiveCall(caller, receiver)
        self._active_calls.append(call)

        if call.is_cross_border:
            self._cross_border_calls_count += 1

        return call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_calls_count
