import pytest
from examples.domain.auth.errors.authentication_errors import (
    PasswordEncryptionError,
    PasswordDecryptionError,
)
from examples.domain.shared.errors import SomethingWentWrongError


class TestAuthenticateUserPasswordEncryptionError:
    """Test cases for password encryption error scenarios."""

    @pytest.mark.asyncio()
    async def test_authenticate_password_encryption_error(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test authentication failure when password encryption raises an
        error."""
        # Arrange
        password_encryption_error = PasswordEncryptionError(
            "Password encryption failed"
        )
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        usecase.password_encryptor.verify_password.side_effect = (
            password_encryption_error
        )

        # Act & Assert
        with pytest.raises(SomethingWentWrongError) as exc_info:
            await usecase.execute()

        # Assert
        assert exc_info.value.__cause__ is password_encryption_error
        usecase.logger.error.assert_awaited_once_with(
            password_encryption_error
        )

    @pytest.mark.asyncio()
    async def test_authenticate_password_decryption_error(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test authentication failure when password decryption raises an
        error."""
        # Arrange
        password_decryption_error = PasswordDecryptionError(
            "Password decryption failed"
        )
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        usecase.password_encryptor.verify_password.side_effect = (
            password_decryption_error
        )

        # Act & Assert
        with pytest.raises(SomethingWentWrongError) as exc_info:
            await usecase.execute()

        # Assert
        assert exc_info.value.__cause__ is password_decryption_error
        usecase.logger.error.assert_awaited_once_with(
            password_decryption_error
        )
