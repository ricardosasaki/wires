import pytest
from examples.domain.auth.errors.authentication_errors import (
    PasswordVerificationError,
)
from examples.domain.shared.errors import SomethingWentWrongError


class TestAuthenticateUserPasswordVerificationError:
    """Test cases for password verification error scenarios."""

    @pytest.mark.asyncio()
    async def test_authenticate_password_verification_error(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test authentication failure when password verification raises an
        error."""
        # Arrange
        uc = usecase
        password_verification_error = PasswordVerificationError(
            "Password verification failed"
        )
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        uc.password_encryptor.verify_password.side_effect = (
            password_verification_error
        )

        # Act & Assert
        with pytest.raises(SomethingWentWrongError) as exc_info:
            await uc.execute()

        # Assert
        assert exc_info.value.__cause__ is password_verification_error
        uc.user_repository.get_active_user.assert_awaited_once_with(
            uc.email
        )
        uc.cryptography_repository.get_settings_for.assert_awaited_once_with(
            uc.email
        )
        uc.password_encryptor.verify_password.assert_called_once_with(
            uc.password,
            mock_user.encrypted_password,
            mock_cryptography_settings,
        )
        uc.logger.error.assert_awaited_once_with(
            password_verification_error
        )
