import pytest
from unittest.mock import MagicMock


class TestAuthenticateUserIntegration:
    """Integration test cases for the authenticate user use case."""

    @pytest.mark.asyncio()
    async def test_authenticate_user_called_user_repository(self, usecase):
        """Test that the user repository is called with correct parameters."""
        # Arrange
        mock_user = MagicMock()
        mock_settings = MagicMock()
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_settings
        )
        usecase.password_encryptor.verify_password.return_value = True

        # Act
        await usecase.execute()

        # Assert
        usecase.user_repository.get_active_user.assert_awaited_once_with(
            usecase.email
        )

    @pytest.mark.asyncio()
    async def test_authenticate_user_called_cryptography_repository(
        self, usecase, mock_user
    ):
        """Test that the cryptography repository is called with correct
        parameters."""
        # Arrange
        mock_settings = MagicMock()
        uc = usecase
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.return_value = (
            mock_settings
        )
        uc.password_encryptor.verify_password.return_value = True

        # Act
        await uc.execute()

        # Assert
        uc.cryptography_repository.get_settings_for.assert_awaited_once_with(
            usecase.email
        )

    @pytest.mark.asyncio()
    async def test_authenticate_user_called_password_encryptor(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test that the password encryptor is called with correct
        parameters."""
        # Arrange
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        usecase.password_encryptor.verify_password.return_value = True

        # Act
        await usecase.execute()

        # Assert
        usecase.password_encryptor.verify_password.assert_called_once_with(
            usecase.password,
            mock_user.encrypted_password,
            mock_cryptography_settings,
        )

    @pytest.mark.asyncio()
    async def test_authenticate_user_logger_not_called_on_success(
        self, usecase, mock_user, mock_cryptography_settings
    ):
        """Test that logger is not called when authentication is successful."""
        # Arrange
        usecase.user_repository.get_active_user.return_value = mock_user
        usecase.cryptography_repository.get_settings_for.return_value = (
            mock_cryptography_settings
        )
        usecase.password_encryptor.verify_password.return_value = True

        # Act
        await usecase.execute()

        # Assert
        usecase.logger.error.assert_not_awaited()

    @pytest.mark.asyncio()
    async def test_authenticate_user_with_different_email_and_password(
        self, usecase
    ):
        """Test authentication with different email and password values."""
        uc = usecase
        # Arrange
        test_email = "test@example.com"
        test_password = "test_password_123"

        # Update the use case with test values
        uc.email = test_email
        uc.password = test_password

        mock_user = MagicMock()
        mock_settings = MagicMock()
        uc.user_repository.get_active_user.return_value = mock_user
        uc.cryptography_repository.get_settings_for.return_value = (
            mock_settings
        )
        uc.password_encryptor.verify_password.return_value = True

        # Act
        result = await usecase.execute()

        # Assert
        assert result is True
        uc.user_repository.get_active_user.assert_awaited_once_with(
            test_email
        )
        uc.cryptography_repository.get_settings_for.assert_awaited_once_with(
            test_email
        )
        uc.password_encryptor.verify_password.assert_called_once_with(
            test_password,
            mock_user.encrypted_password,
            mock_settings,
        )
