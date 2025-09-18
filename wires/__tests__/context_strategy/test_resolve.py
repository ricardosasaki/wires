"""
When a port has multiple adapters and we need to select them on the fly
"""

from wires.strategy import ContextStrategy, Composite

from typing import Protocol


class MockCommunicationStrategy(Protocol):
    def send(self, message: str) -> None:
        ...


class SMSStrategy(MockCommunicationStrategy):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


class EmailStrategy(MockCommunicationStrategy):
    def send(self, message: str) -> None:
        print(f"Sending Email: {message}")


def test_context_strategy_resolve() -> None:
    context_strategy: ContextStrategy[
        MockCommunicationStrategy
    ] = ContextStrategy(
        key="email",
        strategies={
            'email': Composite(EmailStrategy),
            'sms': Composite(SMSStrategy)
        }
    )

    assert isinstance(
        context_strategy.__resolve__(),
        EmailStrategy
    )
