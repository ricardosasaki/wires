import pytest
from examples.domain.auth.errors.authentication_errors import (
    UserNotFoundError,
    AuthenticationError,
)


class TestAuthenticateUserUserNotFound:
    """Test cases for user not found scenarios."""

    @pytest.mark.asyncio()
    async def test_authenticate_user_not_found(self, usecase):
        """Test authentication failure when user is not found."""
        # Arrange
        user_not_found_error = UserNotFoundError("User not found")
        usecase.user_repository.get_active_user.side_effect = (
            user_not_found_error
        )

        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            await usecase.execute()

        # Assert
        assert exc_info.value.__cause__ is user_not_found_error
        usecase.user_repository.get_active_user.assert_awaited_once_with(
            usecase.email
        )
        usecase.logger.error.assert_awaited_once_with(user_not_found_error)
        usecase.cryptography_repository.get_settings_for.assert_not_awaited()
        usecase.password_encryptor.verify_password.assert_not_called()
