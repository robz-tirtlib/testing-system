from dataclasses import dataclass


@dataclass
class UserRegister:
    username: str
    email: str
    password: str


@dataclass
class UserLogin:
    username: str
    password: str
