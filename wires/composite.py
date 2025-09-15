from typing import (
    Generic, TypeVar, Type, Any, Generator, Union, Self
)
from contextlib import contextmanager


T = TypeVar('T', covariant=True)


class DependencyObject(Generic[T]):
    def __init__(self, name: str, dependency: T):
        self.dependency = dependency
        self.name = name

    def __call__(self) -> T:
        return self.dependency


class Composite(Generic[T]):
    """
    Simple implementation of the composite Pattern.
    Used when objects appear to have complex logic of creation
    and is necessary to separate by steps and smaller objects
    to compose.

    # example:
    A simple service class that retrieves a list of skills.
    The skills are stored in a database that can only be retrieved by a
    repository To access the service, a controller is used to build the
    service.

    database_connection: DependencyObject
    repository: Composite[UserRepository] @params: database_connection
    service: Composite[UserService] @params: repository
    controller: Composite[UserController]

    # usage
    ```
    database_connection = DependencyObject(
        "database_connection",
        database_connection
    )
    repository = Composite(
        UserRepository,
        database_connection=database_connection
    )
    service = Composite(UserService, repository=repository)
    controller = Composite(UserController, service=service)

    controller()
    ```

    # In the example above, controller() holds the logic to build the
    # service, but it's not yet instantiated.


    if another connection is needed, you can simply override the dependency
    object and the composite will be re-instantiated with the new dependency.

    ```
    with controller.overrides(
        {
            "database_connection": DependencyObject(
                "database_connection", database_connection_2
            )
        }
    ):
        controller()
    ```
    """
    def __init__(
        self,
        model: Type[T],
        *args: Any,
        **kwargs: Any
    ):
        self.model = model
        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> T:
        if self.args:
            return self.model(*self.args, **self.kwargs)
        return self.model(**self.kwargs)

    @contextmanager
    def overrides(
        self,
        _overrides: dict[str, Union[DependencyObject, Self]]
    ) -> Generator[T, Any, Any]:
        """
        Override the arguments of the composite.
        # Usage example:
        ```
        with composite.overrides({"arg1": "value1"}):
            print(composite.args)
        ```
        """
        try:
            with self._params_overrides(_overrides):
                yield self()
        finally:
            self._args = self.original_args
            self._kwargs = self.original_kwargs

    @classmethod
    def injected(cls, model: Type[T]) -> T:  # type: ignore
        """
        Just a placeholder when injecting dependencies with context.

        # Usage example:
        ```
        @inject(ApplicationContext)
        def any_method(
            controller: Controller = Composite.injected(Controller),
        ) -> Controller:
            return controller
        ```
        """
        return cls(model)  # type: ignore

    @property
    def args(self) -> list[Any]:
        """
        Resolve the arguments of the composite.
        # Usage example:
        ```
        composite = Composite(Model, *args, **kwargs)
        print(composite.args)
        ```
        """
        return [
            self.resolve_composite(arg) for arg in self._args  # type: ignore
        ]

    @property
    def kwargs(self) -> dict[str, Any]:
        """
        Resolve the keyword arguments of the composite.
        # Usage example:
        ```
        composite = Composite(Model, *args, **kwargs)
        print(composite.kwargs)
        ```
        """
        return {
            key: self.resolve_composite(value)
            for key, value in self._kwargs.items()  # type: ignore
        }

    def resolve_composite(self, arg: Union[Self, Any]) -> Union[T, Any]:
        if isinstance(arg, Composite) or isinstance(arg, DependencyObject):
            return arg()
        return arg

    def _override_args(
        self,
        overrides: dict[str, Union[DependencyObject, Self]]
    ) -> list[Any]:
        args = []

        if self._args:
            for arg in self._args:
                if isinstance(arg, DependencyObject):
                    if arg.name in overrides:
                        args.append(overrides[arg.name])
                    else:
                        args.append(arg)
                else:
                    args.append(arg)
        return args

    def _override_kwargs(
        self,
        overrides: dict[str, Union[DependencyObject, Self]]
    ) -> dict[str, Any]:
        kwargs = {}

        if self._kwargs:
            for key, value in self._kwargs.items():
                if isinstance(value, DependencyObject):
                    if value.name in overrides:
                        kwargs[key] = overrides[value.name]
                        continue
                kwargs[key] = value

        return kwargs

    @contextmanager
    def _params_overrides(
        self, overrides: dict[str, Union[DependencyObject, Self]]
    ) -> Generator[
        tuple[list[Any], dict[str, Any]], Any, Any
    ]:
        try:
            self.original_args = self._args
            self.original_kwargs = self._kwargs

            self._args = self._override_args(overrides)  # type: ignore
            self._kwargs = self._override_kwargs(overrides)

            yield self.args, self.kwargs
        finally:
            self._args = self.original_args
            self._kwargs = self.original_kwargs
