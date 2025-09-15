from unittest.mock import MagicMock, AsyncMock
from wires import Context, Composite, DependencyObject
from examples.domain.auth.ports.password_encryptor import PasswordEncryptor
from examples.domain.auth.ports.persistence.cryptography_repository import (
    CryptographyRepository
)
from examples.domain.auth.ports.persistence.user_repository import (
    UserRepository
)
from examples.domain.shared.ports.logger import Logger
from examples.domain.auth.usecases.authenticate_user import AuthenticateUser


class AuthenticationContext(Context):
    email: DependencyObject[str] = DependencyObject("email", "")
    password: DependencyObject[str] = DependencyObject("password", "")

    user_repository: Composite[UserRepository] = Composite(
        MagicMock,
        get_active_user=AsyncMock(return_value=MagicMock())
    )

    password_encryptor: Composite[PasswordEncryptor] = Composite(
        MagicMock,
        verify_password=AsyncMock(return_value=True)
    )

    cryptography_repository: Composite[CryptographyRepository] = Composite(
        MagicMock,
        get_settings_for=AsyncMock(return_value=MagicMock())
    )

    logger: Composite[Logger] = Composite(
        MagicMock,
        error=AsyncMock()
    )

    authenticate_user_usecase: Composite[AuthenticateUser] = Composite(
        AuthenticateUser,
        email,
        password,
        user_repository=user_repository,
        password_encryptor=password_encryptor,
        cryptography_repository=cryptography_repository,
        logger=logger,
    )
