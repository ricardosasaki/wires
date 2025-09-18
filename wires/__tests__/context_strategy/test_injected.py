"""
When a port has multiple adapters and we need to select them on the fly
"""

from wires.strategy import ContextStrategy, Composite
from wires import Context, inject

from typing import Protocol


class MockCommunicationStrategy(Protocol):
    def send(self, message: str) -> str:
        ...


class SMSStrategy(MockCommunicationStrategy):
    def send(self, message: str) -> str:
        return f"Sending SMS: {message}"


class EmailStrategy(MockCommunicationStrategy):
    def send(self, message: str) -> str:
        return f"Sending Email: {message}"


class AppContext(Context):
    notification_type: str = "email"

    communication_strategy: ContextStrategy[
        MockCommunicationStrategy
    ] = ContextStrategy(
        key=notification_type,
        strategies={
            'email': Composite(EmailStrategy),
            'sms': Composite(SMSStrategy)
        }
    )


@inject(AppContext)
def send_notification(
    strategy: MockCommunicationStrategy = None  # type: ignore
) -> str:
    return strategy.send("Hello World!")


def test_context_strategy_injection() -> None:
    assert send_notification() == "Sending Email: Hello World!"
