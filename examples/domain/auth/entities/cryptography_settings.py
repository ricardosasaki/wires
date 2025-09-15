from dataclasses import dataclass


@dataclass
class CryptographySettings:
    algorithm: str
    key: str
    iv: str
