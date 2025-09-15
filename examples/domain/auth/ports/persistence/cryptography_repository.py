from typing import Protocol
from abc import abstractmethod
from examples.domain.auth.entities.cryptography_settings import (
    CryptographySettings
)


class CryptographyRepository(Protocol):
    @abstractmethod
    async def get_settings_for(self, email: str) -> CryptographySettings:
        ...
