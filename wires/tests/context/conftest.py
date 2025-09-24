from dataclasses import dataclass, field
from typing import Protocol
from abc import abstractmethod
from wires import Context, Composite

import pytest


@dataclass
class VariantDependency01:
    data: str = field(default="Variant dependency 01")

    async def do_something_important(self) -> str:
        return "from variant dependency 01"


@dataclass
class Dependency01:
    data: str = field(default="Deep dependency 01")

    async def do_something_important(self) -> str:
        return "from dependency 01"


@dataclass
class Dependency02:
    dependency_01: Dependency01 = field()
    data: str = field(default="Deep dependency 02")


@dataclass
class Dependency03:

    dependency_02: Dependency02
    data: str = field(default="Deep dependency 03")


class MockDependencyProtocol(Protocol):
    @abstractmethod
    def do_something_important(self) -> str:
        ...


class MockContext(Context):
    dependency_01: Composite[Dependency01] = Composite(
        Dependency01
    )
    dependency_02: Composite[Dependency02] = Composite(
        Dependency02,
        dependency_01
    )

    dependency_03: Composite[Dependency03] = Composite(
        Dependency03,
        dependency_02=dependency_02,
    )


@pytest.fixture()
def context():
    _context = MockContext()
    _context.initialize_adapters()

    return _context
