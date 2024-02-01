from dataclasses import dataclass

from .new_types import UserId


@dataclass
class User:
    id: UserId
    username: str
    email: str
