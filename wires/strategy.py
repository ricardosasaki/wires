from typing import Generic, TypeVar, Union
from wires.composite import Composite, DependencyObject


T = TypeVar("T", covariant=True)


class ContextStrategy(Composite[T], Generic[T]):
    def __init__(
        self,
        key: Union[str, DependencyObject[str]],
        strategies: dict[str, Composite[T]],
        *args,
        **kwargs
    ) -> None:
        self.key = key
        self.strategies = strategies
        super().__init__(self, *args, **kwargs)  # type: ignore

    def __resolve__(self) -> T:
        """
        Indicates to context that this object can be
        resolved without any additional information
        """
        return self()

    def __call__(self) -> T:
        """
        Indicates to context that this object can be
        resolved without any additional information
        """
        return self.strategies[str(self.key)]()
