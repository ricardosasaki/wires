class UserNotFoundError(Exception):
    pass


class SettingsNotFoundError(Exception):
    pass


class PasswordEncryptionError(Exception):
    pass


class PasswordDecryptionError(Exception):
    pass


class PasswordVerificationError(Exception):
    pass


class AuthenticationError(Exception):
    pass