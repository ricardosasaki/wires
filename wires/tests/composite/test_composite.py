from wires import Composite
from .conftest import Dependency01, Dependency02


class TestComposite:
    def test_basic_composite_object_creation(self):
        composite = Composite(int)

        assert composite() == 0

    def test_composite_object_with_args(self):
        composite = Composite(
            Dependency01, data="composite test 01"
        )

        assert composite() == Dependency01("composite test 01")

    def test_composite_object_with_kwargs(self):
        composite = Composite(
            Dependency01, data="composite test 01"
        )

        assert composite() == Dependency01(data="composite test 01")

    def test_composite_with_dependencies(self):
        dependency_01 = Composite(
            Dependency01,
            data="composite test 01"
        )
        composite = Composite(
            Dependency02, dependency_01=dependency_01
        )

        assert composite() == Dependency02(
            dependency_01=Dependency01(
                data="composite test 01")
            )

