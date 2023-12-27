from abc import ABC, abstractmethod

from src.domain.models.quiz import Quiz
from src.domain.models.user import User


class IPermissionService(ABC):
    @abstractmethod
    def user_can_update_quiz_settings(
        self, user: User, quiz: Quiz,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def user_can_get_quiz_data(
        self, user: User, quiz: Quiz, accessed_via_private_link: bool,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def user_can_get_quiz_full_data(
        self, user: User, quiz: Quiz, accessed_via_private_link: bool,
    ) -> bool:
        raise NotImplementedError


class PermissionService(IPermissionService):
    def user_can_update_quiz_settings(self, user: User, quiz: Quiz) -> bool:
        if user.id != quiz.creator_id:
            return False
        return True

    def user_can_get_quiz_data(
            self, user: User, quiz: Quiz, accessed_via_private_link: bool
    ) -> bool:
        if quiz.private_link is not None:
            if not accessed_via_private_link:
                return False

        if not quiz.is_active and user.id != quiz.creator_id:
            return False
        return True

    def user_can_get_quiz_full_data(
            self, user: User, quiz: Quiz, accessed_via_private_link: bool
    ) -> bool:
        if quiz.private_link is not None:
            if not accessed_via_private_link:
                return False
        return user.id == quiz.creator_id
