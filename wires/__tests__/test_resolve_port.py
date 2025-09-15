from wires import Context, Port
from abc import abstractmethod
from wires.composite import Composite, DependencyObject


class RepositoryPort(Port):
    exchangable_dependency: str

    @abstractmethod
    def get_all(self) -> list[str]:
        ...


class RepositoryAdapter(RepositoryPort):
    def __init__(
        self,
        conn: str,
        random_dependency: str,
        exchangable_dependency: str
    ):
        self.conn = conn
        self.random_dependency = random_dependency
        self.exchangable_dependency = exchangable_dependency

    def get_all(self) -> list[str]:
        return ["Python", "JavaScript"]


class Service:
    def __init__(self, repository: RepositoryPort):
        self.repository = repository

    def exchangable_dependency(self) -> str:
        return self.repository.exchangable_dependency


class ApplicationContext(Context):
    random_dependency: str = "random_dependency"
    exchangable_dependency: DependencyObject[str] = DependencyObject(
        "exchangable_dependency", "Hello"
    )
    repository: Composite[RepositoryPort] = Composite(
        RepositoryAdapter,
        conn="sqlite://",
        random_dependency=random_dependency,
        exchangable_dependency=exchangable_dependency
    )
    service: Composite[Service] = Composite(
        Service,
        repository=repository
    )


def test_resolve_port() -> None:
    context = ApplicationContext()
    context.initialize_adapters()

    repository_adapter: RepositoryAdapter = context.resolve_port(
        RepositoryPort
    )

    assert repository_adapter.get_all() == ["Python", "JavaScript"]
    assert repository_adapter.conn == "sqlite://"
    assert repository_adapter.random_dependency == "random_dependency"


def test_resolve_port_with_changed_dependencies() -> None:
    context = ApplicationContext()
    context.initialize_adapters()

    context.random_dependency = "new dependency"

    repository_adapter: RepositoryAdapter = context.resolve_port(
        RepositoryPort
    )

    assert repository_adapter.get_all() == ["Python", "JavaScript"]
    assert repository_adapter.conn == "sqlite://"
    assert repository_adapter.random_dependency == "random_dependency"
    assert repository_adapter.exchangable_dependency == "Hello"

    repository_adapter = context.resolve_port(
        RepositoryPort,
        overrides={"exchangable_dependency": "World"}
    )
    assert repository_adapter.exchangable_dependency == "World"

    service = context.resolve_port(Service)
    assert service.exchangable_dependency() == "Hello"
