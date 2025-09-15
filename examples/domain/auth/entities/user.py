from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    name: str
    email: str

    encrypted_password: str
    created_at: datetime
    updated_at: datetime
