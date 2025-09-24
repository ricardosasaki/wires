from .conftest import Dependency01, Dependency02


class TestResolve:
    def test_resolve_dependency01(self, context):
        assert isinstance(
            context.resolve(
                Dependency01
            ), Dependency01
        )

    def test_resolve_dependency02(self, context):
        dependency_02 = context.resolve(Dependency02)
        assert isinstance(dependency_02, Dependency02)
        assert isinstance(dependency_02.dependency_01, Dependency01)
