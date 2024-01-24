from abc import ABC, abstractmethod

from src.domain.models.new_types import QuizId, UserId, QuizPassId
from src.domain.models.quiz import Quiz, QuizSettingsFull

from src.domain.models.quiz_pass import QuizPass, QuizPassCreate


class IQuizRepo(ABC):
    @abstractmethod
    def get_quiz_by_id(self, quiz_id: QuizId) -> Quiz | None:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_by_link(self, private_link: str) -> Quiz | None:
        raise NotImplementedError

    @abstractmethod
    def create_quiz(
        self, quiz_settings: QuizSettingsFull, user_id: UserId,
    ) -> Quiz:
        raise NotImplementedError

    @abstractmethod
    def update_is_active(
        self, quiz_id: QuizId, change_to_active: bool
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_quiz_settings(
        self, quiz_id: QuizId, quiz_settings: QuizSettingsFull,
    ) -> None:
        raise NotImplementedError


class IQuizPassRepo(ABC):
    @abstractmethod
    def get_quiz_pass_by_id(self, quiz_pass_id: QuizPassId) -> QuizPass | None:
        raise NotImplementedError

    @abstractmethod
    def create_quiz_pass(self, quiz_pass: QuizPassCreate) -> QuizPass:
        raise NotImplementedError

    @abstractmethod
    def finish_quiz_pass(self, quiz_pass_id: QuizPassId) -> None:
        raise NotImplementedError
