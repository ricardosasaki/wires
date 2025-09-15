import pytest
from examples.domain.auth.errors.authentication_errors import (
    SettingsNotFoundError,
    AuthenticationError,
)


class TestAuthenticateUserSettingsNotFound:
    """Test cases for cryptography settings not found scenarios."""

    @pytest.mark.asyncio()
    async def test_authenticate_settings_not_found(
        self, usecase, mock_user
    ):
        """Test authentication failure when cryptography settings are not
        found."""
        # Arrange
        uc = usecase
        settings_not_found_error = SettingsNotFoundError(
            "Settings not found"
        )
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.side_effect = (
            settings_not_found_error
        )

        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            await uc.execute()

        # Assert
        assert exc_info.value.__cause__ is settings_not_found_error
        uc.user_repository.get_active_user.assert_awaited_once_with(
            uc.email
        )
        uc.cryptography_repository.get_settings_for.assert_awaited_once_with(
            uc.email
        )
        uc.logger.error.assert_awaited_once_with(
            settings_not_found_error
        )
        uc.password_encryptor.verify_password.assert_not_called()
