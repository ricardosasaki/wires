import pytest
from unittest.mock import MagicMock, AsyncMock
from examples.domain.auth.tests.context import AuthenticationContext
from examples.domain.auth.usecases.authenticate_user import AuthenticateUser
from examples.domain.auth.entities.user import User
from examples.domain.auth.entities.cryptography_settings import (
    CryptographySettings,
)
from datetime import datetime


@pytest.fixture()
def context():
    context = AuthenticationContext()
    context.initialize_adapters()

    return context


@pytest.fixture
def usecase():
    """Create an AuthenticateUser use case with mocked dependencies."""
    context = AuthenticationContext()
    context.initialize_adapters()
    usecase = context.resolve_port(AuthenticateUser)
    
    # Set up default mock behaviors
    usecase.user_repository.get_active_user = AsyncMock()
    usecase.cryptography_repository.get_settings_for = AsyncMock()
    usecase.password_encryptor.verify_password = MagicMock()
    usecase.logger.error = AsyncMock()
    
    return usecase


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    return User(
        name="John Doe",
        email="john@example.com",
        encrypted_password="encrypted_password_123",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def mock_cryptography_settings():
    """Create mock cryptography settings for testing."""
    return CryptographySettings(
        algorithm="fernet",
        key="test_key_123",
        iv="test_iv_123",
    )
