from abc import ABC, abstractmethod

from src.domain.models.new_types import (
    AnswerId, QuestionId, QuizId, UserId, QuizPassId,
)
from src.domain.models.quiz import Quiz, QuizSettings
from src.domain.models.answer import UserAnswer

from src.domain.models.quiz_pass import (
    QuizPass, QuizPassCreate, QuizPassResult,
)


class IQuizRepo(ABC):
    @abstractmethod
    def get_quiz_by_id(self, quiz_id: QuizId) -> Quiz | None:
        raise NotImplementedError

    @abstractmethod
    def get_owner_id(self, quiz_id: QuizId) -> UserId | None:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_by_link(self, private_link: str) -> Quiz | None:
        raise NotImplementedError

    @abstractmethod
    def create_quiz(
        self, quiz_settings: QuizSettings, user_id: UserId,
        title: str,
    ) -> Quiz:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_settings(self, quiz_id: QuizId) -> QuizSettings:
        raise NotImplementedError

    @abstractmethod
    def update_is_active(
        self, quiz_id: QuizId, change_to_active: bool
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_quiz_settings(
        self, quiz_id: QuizId, quiz_settings: QuizSettings,
    ) -> None:
        raise NotImplementedError


class IQuizPassRepo(ABC):
    @abstractmethod
    def get_quiz_pass_result(
        self, quiz_pass_id: QuizPassId,
    ) -> QuizPassResult | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_id(self, quiz_pass_id: QuizPassId) -> UserId | None:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_pass_by_id(self, quiz_pass_id: QuizPassId) -> QuizPass | None:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_id(self, quiz_pass_id: QuizPassId) -> QuizId | None:
        raise NotImplementedError

    @abstractmethod
    def create_quiz_pass(self, quiz_pass: QuizPassCreate) -> QuizPass:
        raise NotImplementedError

    @abstractmethod
    def finish_quiz_pass(self, quiz_pass_id: QuizPassId) -> None:
        raise NotImplementedError

    @abstractmethod
    def write_answer(
        self, quiz_pass_id: QuizPassId, question_id: QuestionId,
        user_id: UserId, choice_answers: list[AnswerId] | None,
        no_choice_answer: str | None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user_answers(self, quiz_pass_id: QuizPassId) -> list[UserAnswer]:
        raise NotImplementedError
