from examples.services.authenticate_service import AuthenticateService
from examples.domain.auth.usecases.authenticate_user import AuthenticateUser
import pytest


@pytest.mark.asyncio
class TestAuthenticateService:
    async def test_injected_correctly(self):
        authenticate_service = AuthenticateService()
        await authenticate_service.authenticate(
            "test@test.com", "password"
        )

        assert isinstance(authenticate_service.usecase, AuthenticateUser)
        assert authenticate_service.usecase.email == "test@test.com"
        assert authenticate_service.usecase.password == "password"
