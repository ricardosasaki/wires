from .context import Context
from .context_registry import ContextRegistry
from .parameters import ParameterOverrider
from typing import Callable, Any
import functools


def inject(
    context: type[Context]
):
    def wrapper(
        func: Callable
    ):
        @functools.wraps(func)
        def inner(*args, **kwargs) -> Any:
            _context = ContextRegistry.get_instance(context)
            _context.initialize_adapters()

            dependencies = _context.resolve_dependencies(func)
            parameters = ParameterOverrider(
                func,
                default_args=list(args),
                default_kwargs=kwargs
            )
            _args = parameters.override_args(dependencies)
            _kwargs = parameters.override_kwargs(dependencies)

            return func(
                *_args,
                **_kwargs
            )
        return inner
    return wrapper
