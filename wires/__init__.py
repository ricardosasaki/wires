"""
Wires is a simple dependency injection implementation
that allows you to create complex compositions of objects
by defining the dependencies of the objects and the way to resolve them.

Also, it gives a clear interface of how you can code can depend on abstractions
instead of concrete implementations.


# Define your objects:
```
class ApplicationContext(Context):
    repository: Composite[RepositoryProtocol] = Composite(
        RepositoryAdapter,
        conn="sqlite://"
    )
    service: Composite[ServiceProtocol] = Composite(
        ServiceAdapter,
        repository=repository
    )
    controller: Composite[Controller] = Composite(
        Controller,
        service=service
    )
```

# Use them:
```
context = ApplicationContext()
context.initialize_adapters()

controller: Controller = context.resolve(Controller)
repository: RepositoryProtocol = context.resolve(RepositoryProtocol)
```

# or use them by injecting direct into your functions:
```
@inject(ApplicationContext)
def main(
    controller: Controller = Composite.injected(Controller),
) -> Controller:
    controller.very_cool_method()
```
"""


from typing import (
    Protocol, runtime_checkable, TypeVar, Callable, Type, Any,
    Union, Optional
)
from .composite import Composite, DependencyObject
from .strategy import ContextStrategy
import inspect
import functools
from threading import current_thread

from .__version__ import __version__

__all__ = [
    "Port",
    "Adapter",
    "Context",
    "ContextRegistry",
    "Composite",
    "DependencyObject",
    "inject",
    "__version__",
]

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)


@runtime_checkable
class Port(Protocol[T]):

    @classmethod
    def injected(cls, port: Type[T]) -> T:  # type: ignore
        return None  # type: ignore


class Adapter():
    def __class_getitem__(cls, item: Type[T]) -> T:
        return None  # type: ignore


class Context:
    def __init__(self):
        self.adapters = {}
        self.adapters_initialized = False

    def overrides(self, overrides: dict[str, Any]) -> Any:
        for key, value in overrides.items():
            if key in self.adapters:
                if (
                    isinstance(value, Composite)
                    or isinstance(value, DependencyObject)
                ):
                    self.adapters[
                        self.composite_key(value)  # type: ignore
                    ] = value
                else:
                    self.adapters[key] = DependencyObject(key, value)

    def _resolve_positional_argument(
        self,
        index: int,
        key: str,
        value: Any,
        args: list[Any],
        kwargs: dict[str, Any],
        positional_arguments_count: int
    ) -> tuple[list[str], dict[str, Any]]:
        if index < positional_arguments_count:
            args[index] = value
        else:
            kwargs[key] = value

        return args, kwargs

    def resolve_dependencies(
        self,
        model: Callable,
        args: list[Any],
        kwargs: dict[str, Any]
    ) -> tuple[list[str], dict[str, Any]]:
        data = inspect.getfullargspec(model)
        positional_arguments = len(args)

        for index, arg in enumerate(data.args):
            dependency = data.annotations.get(arg)
            adapter = None

            # Check if this is an Adapter placeholder
            if (dependency and hasattr(dependency, '__origin__') and
                    dependency.__origin__ is Adapter):
                # For Adapter[SomeType], we need to resolve SomeType
                if (hasattr(dependency, '__args__') and
                        dependency.__args__):
                    target_type = dependency.__args__[0]
                    adapter = self.resolve(target_type)
                else:
                    adapter = self.get_constructor_value(
                        args, kwargs, arg, index
                    )
            elif dependency is not None:
                adapter = self.resolve(dependency)

            if adapter is None:
                adapter = self.get_constructor_value(
                    args, kwargs, arg, index
                )

            args, kwargs = self._resolve_positional_argument(
                index, arg, adapter, args, kwargs, positional_arguments
            )

        return args, kwargs

    def initialize_adapters(self):
        if self.adapters_initialized:
            return True

        data = inspect.get_annotations(self.__class__)
        for key, value in data.items():
            if (
                hasattr(value, '__origin__')
                and (
                    value.__origin__ == Composite
                    or value.__origin__ == ContextStrategy
                )
            ):
                if value.__args__:
                    port = value.__args__[0]
                    self.adapters[self.composite_key(port)] = getattr(
                        self, key
                    )

        self.adapters_initialized = True

    def composite_key(self, port: Type[Union[Port[T], T]]) -> Optional[str]:
        return f"{port.__module__}.{port.__name__}"

    def resolve(
        self, port: Type[Union[Port[T], T]],
        overrides: Optional[dict[str, Any]] = None
    ) -> Union[T, Any]:
        adapter = self.get_adapter(port)
        if isinstance(adapter, Composite):
            with adapter.overrides(overrides or {}) as _adapter:
                return _adapter
        return adapter

    def get_adapter(
        self, port: Type[Union[Port[T], T]]
    ) -> Union[T, Any]:
        composite_key = self.composite_key(port)
        if composite_key in self.adapters:
            return self.adapters[composite_key]
        return None

    def get_constructor_value(
        self, args: list[Any], kwargs: dict[str, Any], key: str, index: int
    ) -> Any:
        if index < len(args):
            return args[index]
        else:
            return kwargs.get(key)

    def inject_dependencies(
        self,
        model: Callable,
        _args: tuple[Any, ...],
        _kwargs: dict[str, Any]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        args, kwargs = self.resolve_dependencies(model, list(_args), _kwargs)
        return tuple(args), kwargs


class ContextRegistry:
    instance_registry: dict[str, Context] = {}

    @classmethod
    def get_instance(cls, context: Type[Context]) -> Context:
        _current_thread = current_thread()
        key = (str(_current_thread.ident) or
               f"{context.__class__.__name__}-{context.__class__.__module__}")
        if key not in cls.instance_registry:
            cls.instance_registry[key] = context()
        return cls.instance_registry[key]


def inject(context: Type[Context]):
    _context = ContextRegistry.get_instance(context)
    _context.initialize_adapters()

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            _args, _kwargs = _context.inject_dependencies(
                func, args, kwargs
            )
            return func(*_args, **_kwargs)
        return inner
    return wrapper
