from threading import current_thread
from typing import Generic, TypeVar


T = TypeVar('T')


class ContextRegistry(Generic[T]):
    instance_registry: dict[str, T] = {}

    @classmethod
    def get_instance(cls, context: type[T]) -> T:
        _current_thread = current_thread()
        thread_ident = _current_thread.ident if _current_thread else 0
        ctx_name = context.__name__ if context else "default"
        ctx_mod = context.__module__ if context else "default"

        key = f"{ctx_mod}.{ctx_name}-{thread_ident}"

        if key not in cls.instance_registry:
            cls.instance_registry[key] = context()
        return cls.instance_registry[key]  # type: ignore
