from typing import Protocol
from abc import abstractmethod
from examples.domain.auth.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def get_active_user(self, email: str) -> User:
        ...

    @abstractmethod
    async def authenticate(self, user: User, password: str) -> bool:
        ...
