from typing import (
    TypeVar, Callable, Type, Any,
    Union, runtime_checkable,
    get_args, get_origin, Generic,
    Protocol
)
from .composite import Composite, DependencyObject
import inspect


__all__ = [
    "Context",
    "Composite",
    "DependencyObject",
]


T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


@runtime_checkable
class Resolvable(Protocol[T_co]):
    """
    One of the basis for the context structure,
    it indicates that the object should be resolved by the context
    and also allows a ways to override dependencies or initialize resources
    """
    def __resolve__(self) -> T_co:
        ...


class Adapter(Generic[T_co]):
    """
    Adapter is an object that was resolved by the Context.
    """

    adapter: Resolvable[T_co] | Any

    def __init__(self, adapter: type[T_co], composite_key: str):
        self.adapter = adapter
        self.composite_key = composite_key

        def __resolve__(self) -> T_co | Any:
            if isinstance(self.adapter, Resolvable):
                return self.adapter.__resolve__()
            return self.adapter


class Context:
    def __init__(self, autoinject: bool = True):
        self.adapters: dict[str, Adapter] = {}
        self.adapters_initialized = False
        self.autoinject = autoinject

    def resolve_dependencies(
        self,
        model: Callable,
    ) -> dict[str, Any]:
        signature = inspect.signature(model)
        solved_dependencies = {}

        for parameter in signature.parameters.values():
            adapter = self.get_adapter(parameter.annotation)
            if adapter:
                solved_dependencies[
                    adapter.composite_key
                ] = adapter.adapter.__resolve__()

        return solved_dependencies

    def initialize_adapters(self):
        data = inspect.get_annotations(self.__class__)
        for key, value in data.items():
            if isinstance(get_origin(value), Resolvable):
                args = get_args(value)
                if args:
                    composite_key = self.composite_key(args[0])
                else:
                    composite_key = self.composite_key(value)
                if composite_key:
                    self.adapters[str(composite_key)] = Adapter(
                        adapter=getattr(self, key),
                        composite_key=composite_key
                    )

        self.adapters_initialized = True

    def composite_key(self, port: Type[T]) -> str | None:
        """
        Builds a composite key that represents the type of the dependency

        Some types may have annotations, in that case, the first argument
        is the always the main dependency
        """

        args = get_args(port)
        if args:
            _port = args[0]
        else:
            _port = port

        if isinstance(_port, type):
            return f"{_port.__module__}.{_port.__name__}"
        return None

    def resolve(
        self,
        dependency: Type[T_co],
    ) -> Union[T_co, Any]:
        adapter: Adapter | None = self.get_adapter(dependency)
        if adapter is None:
            return None

        return adapter.adapter.__resolve__()

    def get_adapter(
        self, port: type[T]
    ) -> Adapter[T] | None:
        composite_key = self.composite_key(port)
        if composite_key in self.adapters:
            return self.adapters[composite_key]
        return None

