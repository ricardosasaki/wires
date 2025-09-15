from examples.domain.auth.ports.password_encryptor import PasswordEncryptor
from examples.domain.auth.ports.persistence.user_repository import (
    UserRepository
)
from examples.domain.auth.ports.persistence.cryptography_repository import (
    CryptographyRepository
)
from examples.domain.auth.errors.authentication_errors import (
    UserNotFoundError,
    SettingsNotFoundError,
    PasswordVerificationError,
    PasswordEncryptionError,
    PasswordDecryptionError,
    AuthenticationError
)
from examples.domain.shared.errors import SomethingWentWrongError
from examples.domain.shared.ports.logger import Logger


class AuthenticateUser:
    def __init__(
        self,
        email: str,
        password: str,
        user_repository: UserRepository,
        cryptography_repository: CryptographyRepository,
        password_encryptor: PasswordEncryptor,
        logger: Logger
    ):
        self.email = email
        self.password = password

        self.logger = logger
        self.user_repository = user_repository
        self.cryptography_repository = cryptography_repository
        self.password_encryptor = password_encryptor

    async def execute(self):
        try:
            user = await self.user_repository.get_active_user(self.email)
            settings = await self.cryptography_repository.get_settings_for(
                self.email
            )

            return self.password_encryptor.verify_password(
                self.password,
                user.encrypted_password,
                settings
            )
        except (UserNotFoundError, SettingsNotFoundError) as e:
            await self.logger.error(e)
            raise AuthenticationError(e) from e
        except (
            PasswordVerificationError,
            PasswordEncryptionError,
            PasswordDecryptionError
        ) as e:
            await self.logger.error(e)
            raise SomethingWentWrongError(e) from e
