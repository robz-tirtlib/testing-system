from abc import ABC, abstractmethod
from src.domain.models.user import UserId, User


class UserRepo(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_username(self, username: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError
