import pytest


class TestAuthenticateUserSuccess:
    """Test cases for successful authentication scenarios."""

    @pytest.mark.asyncio()
    async def test_authenticate_user_success(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test successful authentication with valid credentials."""
        # Arrange
        uc = usecase
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        uc.password_encryptor.verify_password.return_value = True

        # Act
        result = await uc.execute()

        # Assert
        assert result is True
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

    @pytest.mark.asyncio()
    async def test_authenticate_user_password_verification_false(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test authentication when password verification returns False."""
        # Arrange
        uc = usecase
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        uc.password_encryptor.verify_password.return_value = False

        # Act
        result = await uc.execute()

        # Assert
        assert result is False
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
