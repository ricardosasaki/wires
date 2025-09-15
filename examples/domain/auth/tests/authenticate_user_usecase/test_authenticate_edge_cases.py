import pytest
from examples.domain.auth.errors.authentication_errors import (
    UserNotFoundError,
    AuthenticationError,
)


class TestAuthenticateUserEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.asyncio()
    async def test_authenticate_user_with_empty_email(self, usecase):
        """Test authentication with empty email."""
        # Arrange

        usecase.email = ""
        user_not_found_error = UserNotFoundError("User not found")
        usecase.user_repository.get_active_user.side_effect = (
            user_not_found_error
        )

        # Act & Assert
        with pytest.raises(AuthenticationError):
            await usecase.execute()

        # Assert
        usecase.user_repository.get_active_user.assert_awaited_once_with("")

    @pytest.mark.asyncio()
    async def test_authenticate_user_with_empty_password(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test authentication with empty password."""
        # Arrange
        usecase.password = ""
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        usecase.password_encryptor.verify_password.return_value = False

        # Act
        result = await usecase.execute()

        # Assert
        assert result is False
        usecase.password_encryptor.verify_password.assert_called_once_with(
            "",
            mock_user.encrypted_password,
            mock_cryptography_settings,
        )

    @pytest.mark.asyncio()
    async def test_authenticate_user_repository_exception_propagation(
        self, usecase
    ):
        """Test that unexpected exceptions from user repository are
        propagated."""
        # Arrange
        unexpected_error = Exception("Unexpected error")
        usecase.user_repository.get_active_user.side_effect = unexpected_error

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await usecase.execute()

        # Assert
        assert exc_info.value is unexpected_error
