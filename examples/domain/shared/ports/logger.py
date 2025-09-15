from typing import Protocol
from abc import abstractmethod


class Logger(Protocol):

    @abstractmethod
    async def error(self, error: Exception):
        ...