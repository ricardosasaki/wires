from wires import Context, Port, inject
from abc import abstractmethod
from wires.composite import Composite


class RepositoryPort(Port):
    @abstractmethod
    def get_all(self) -> list[str]:
        ...


class Service:
    def __init__(self, repository: RepositoryPort):
        self.repository = repository

    def get_all(self) -> list[str]:
        return self.repository.get_all()


class Controller:
    def __init__(self, service: Service):
        self.service = service

    def get_all(self) -> list[str]:
        return self.service.get_all()


class RepositoryAdapter(RepositoryPort):
    conn: str

    def __init__(self, conn: str):
        self.conn = conn

    def get_all(self) -> list[str]:
        return ["Python", "JavaScript"]


class ApplicationContext(Context):
    repository: Composite[RepositoryPort] = Composite(
        RepositoryAdapter,
        conn="sqlite://"
    )

    service: Composite[Service] = Composite(
        Service,
        repository=repository
    )

    controller: Composite[Controller] = Composite(
        Controller,
        service=service
    )


@inject(ApplicationContext)
def any_method(
    arg1,
    arg2,
    controller: Controller = Composite.injected(Controller),
    name: str = "Art3emis"
) -> Controller | None:
    return controller


def test_inject_with_repository() -> None:
    controller: Controller | None = any_method(1, 2)

    assert controller is not None
    assert isinstance(controller.service, Service)
    assert isinstance(controller.service.repository, RepositoryAdapter)
