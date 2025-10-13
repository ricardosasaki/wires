from wires import inject
from .conftest import Dependency01, MockContext


@inject(
    MockContext,
)
def subject(arg1, arg2, name: str, port: type[Dependency01]):
    return arg1, arg2, name, port


class TestInject:
    def test_inject_with_context(self, context: MockContext):
        result = subject(
            1, 2, "test"
        )

        assert result == (1, 2, "test", Dependency01("Deep dependency 01"))

    def test_inject_with_keyword_arguments(self, context: MockContext):
        result = subject(
            1, arg2=2, name="test"
        )

        assert result == (1, 2, "test", Dependency01("Deep dependency 01"))
