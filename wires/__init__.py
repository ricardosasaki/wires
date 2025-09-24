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

from .context import Context, Adapter
from .context_registry import ContextRegistry
from .composite import Composite
from .strategy import ContextStrategy
from .inject import inject


__all__ = [
    "Context",
    "inject",
    "ContextRegistry",
    "ContextStrategy",
    "Composite",
    "Adapter",
    "Port"
]
