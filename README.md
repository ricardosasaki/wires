# Wires

A simple and elegant dependency injection implementation for Python that allows you to create complex compositions of objects by defining their dependencies and resolution strategies.

## Installation

```bash
 pip install git+https://github.com/ricardosasaki/wires.git@main
```

## Quick Start

### 1. Define Your Interfaces

```python
from typing import Protocol
from wires import Port, Composite, Context, inject

class UserRepository(Protocol):
    def get_user(self, user_id: int) -> dict:
        ...

class UserService(Protocol):
    def get_user_profile(self, user_id: int) -> dict:
        ...

class UserController:
    def __init__(self, service: UserService):
        self.service = service
    
    def handle_request(self, user_id: int) -> dict:
        return self.service.get_user_profile(user_id)
```

### 2. Create Your Implementations

```python
class DatabaseUserRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def get_user(self, user_id: int) -> dict:
        # Your database logic here
        return {"id": user_id, "name": "John Doe"}

class UserServiceImplementation:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def get_user_profile(self, user_id: int) -> dict:
        user = self.repository.get_user(user_id)
        return {"profile": user, "status": "active"}
```

### 3. Configure Your Application Context

```python
class ApplicationContext(Context):
    repository: Composite[UserRepository] = Composite(
        DatabaseUserRepository,
        connection_string="sqlite:///app.db"
    )
    service: Composite[UserService] = Composite(
        UserServiceImplementation,
        repository=repository
    )
    controller: Composite[UserController] = Composite(
        UserController,
        service=service
    )
```

### 4. Use Your Components

#### Direct Resolution

```python
# Initialize the context
context = ApplicationContext()
context.initialize_adapters()

# Resolve components
controller = context.resolve(UserController)
result = controller.handle_request(123)
```

#### Dependency Injection

```python
@inject(ApplicationContext)
def handle_user_request(
    user_id: int,
    controller: UserController = Composite.injected(UserController)
) -> dict:
    return controller.handle_request(user_id)

# Usage
result = handle_user_request(123)
```


### Key Methods

- `Context.initialize_adapters()`: Initialize all composite adapters
- `Context.resolve(port)`: Resolve a dependency by its type
- `Composite.overrides(overrides)`: Context manager for dependency overrides
- `inject(context)`: Decorator for automatic dependency injection

## Development

### Setup Development Environment

```bash
git clone https://github.com/ricardosasaki/wires.git
cd wires
poetry install
```

### Run Tests

```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
