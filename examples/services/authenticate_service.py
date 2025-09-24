from examples.domain.auth.usecases.authenticate_user import AuthenticateUser
from wires import inject, Composite
from examples.domain.auth.tests.context import AuthenticationContext


class AuthenticateService:

    @inject(AuthenticationContext)
    def __init__(
        self,
        usecase: AuthenticateUser
    ):
        self.usecase = usecase

    def authenticate(self, email: str, password: str):
        self.usecase.email = email
        self.usecase.password = password
        return self.usecase.execute()
