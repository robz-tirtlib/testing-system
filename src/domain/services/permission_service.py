from abc import ABC, abstractmethod

from src.domain.models.quiz import Quiz
from src.domain.models.user import User


class IPermissionService(ABC):
    @abstractmethod
    def user_can_update_quiz_settings(
        self, user: User, quiz: Quiz,
    ) -> bool:
        raise NotImplementedError


class PermissionService(IPermissionService):
    def user_can_update_quiz_settings(self, user: User, quiz: Quiz) -> bool:
        if user.id != quiz.creator_id:
            return False
        return True
