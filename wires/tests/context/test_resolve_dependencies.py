from .conftest import (
    MockContext, Dependency01, Dependency02, Dependency03
)


class TestResolveDependencies:
    def test_resolve_dependency_01(self, context: MockContext):
        def _(arg1, arg2, name: str, port: Dependency01):
            return (
                arg1,
                arg2,
                name,
                port
            )

        dependencies = context.resolve_dependencies(_)
        assert 'context.conftest.Dependency01' in dependencies
        adapter = dependencies['context.conftest.Dependency01']
        assert adapter.data == "Deep dependency 01"

    def test_resolve_dependency_02(self, context: MockContext):
        def _(arg1, arg2, name: str, port: Dependency02):
            return (
                arg1,
                arg2,
                name,
                port
            )

        dependencies = context.resolve_dependencies(_)
        assert 'context.conftest.Dependency02' in dependencies

        adapter = dependencies['context.conftest.Dependency02']
        assert adapter.data == "Deep dependency 02"
        assert adapter.dependency_01.data == "Deep dependency 01"

    def test_resolve_dependency_03(self, context: MockContext):
        def _(arg1, arg2, name: str, port: Dependency03):
            return (
                arg1,
                arg2,
                name,
                port
            )

        dependencies = context.resolve_dependencies(_)
        assert 'context.conftest.Dependency03' in dependencies

        adapter = dependencies['context.conftest.Dependency03']
        assert adapter.data == "Deep dependency 03"
        assert adapter.dependency_02.data == "Deep dependency 02"
        assert adapter.dependency_02.dependency_01.data == "Deep dependency 01"
