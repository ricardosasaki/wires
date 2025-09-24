from wires import Composite


class TestCompositeKey:
    def test_composite_key_with_self(self, context):
        assert context.composite_key(
            self.__class__
        ) == 'context.test_composite_key.TestCompositeKey'

    def test_composite_key_with_composite(self, context):
        assert context.composite_key(
            Composite[self.__class__]
        ) == 'context.test_composite_key.TestCompositeKey'
