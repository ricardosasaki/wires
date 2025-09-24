from typing import Callable, Any, get_args, TypeVar
import inspect


T = TypeVar('T')


class ParameterOverrider:
    def __init__(
        self,
        func: Callable,
        default_args: list[Any],
        default_kwargs: dict[str, Any],
    ):
        self.func = func
        self.default_args = default_args
        self.default_kwargs = default_kwargs
        self.parameters = inspect.signature(func).parameters

    def is_positional(self, parameter: inspect.Parameter) -> bool:
        return (
            parameter.kind == inspect.Parameter.POSITIONAL_ONLY
            or parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        )

    def is_keyword_parameter(self, parameter: inspect.Parameter) -> bool:
        return (
            parameter.kind == inspect.Parameter.KEYWORD_ONLY
            or parameter.kind == inspect.Parameter.VAR_KEYWORD
        )

    def composite_key(self, port: type[T]) -> str | None:
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

    def override_args(self, new_args: dict[str, Any]) -> list[Any]:
        args = []
        for index, (name, parameter) in enumerate(self.parameters.items()):
            if self.is_positional(parameter):
                if parameter.annotation:
                    key = self.composite_key(parameter.annotation)
                    if key and new_args.get(key):
                        args.append(new_args[key])
                        continue

                    args.append(
                        self.default_args[index]
                    )

        return args

    def override_kwargs(self, new_kwargs: dict[str, Any]) -> dict[str, Any]:
        kwargs = {}

        for name, parameter in self.parameters.items():
            if self.is_keyword_parameter(parameter):
                if parameter.annotation:
                    key = self.composite_key(parameter.annotation)
                    if key and new_kwargs.get(key):
                        kwargs[name] = new_kwargs[key]
                        continue

                kwargs[name] = self.default_kwargs.get(name)
        return kwargs
