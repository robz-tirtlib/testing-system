from dataclasses import dataclass
from typing import NewType


UserId = NewType("UserId", int)


@dataclass
class User:
    id: UserId
    username: str
    email: str
    password: str


@dataclass
class UserData:
    id: UserId
    username: str
    email: str


@dataclass
class UserRegister:
    username: str
    email: str
    password: str


@dataclass
class UserLogin:
    username: str
    password: str
