from typing import Protocol

from examples.domain.auth.entities.cryptography_settings import (
    CryptographySettings,
)


class PasswordEncryptor(Protocol):
    """Protocol for password encryption and decryption operations."""

    def encrypt_password(
        self, password: str, settings: CryptographySettings
    ) -> str:
        """Encrypt a password using the provided cryptography settings."""
        ...

    def decrypt_password(
        self, encrypted_password: str, settings: CryptographySettings
    ) -> str:
        """Decrypt a password using the provided cryptography settings."""
        ...

    def verify_password(
        self,
        password: str,
        encrypted_password: str,
        settings: CryptographySettings,
    ) -> bool:
        """Verify if a password matches the encrypted password."""
        ...
