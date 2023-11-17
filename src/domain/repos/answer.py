from abc import ABC, abstractmethod

from src.domain.models.new_types import AnswerId, QuestionId
from src.domain.models.answer import Answer, AnswerCreate


class IAnswerRepo(ABC):
    @abstractmethod
    def get_answer_by_id(self, answer_id: AnswerId) -> Answer | None:
        raise NotImplementedError

    @abstractmethod
    def get_answers_by_question_id(
        self, question_id: QuestionId
    ) -> list[Answer]:
        raise NotImplementedError

    @abstractmethod
    def create_answers(
        self, answers: list[AnswerCreate], question_id: QuestionId,
    ) -> list[Answer]:
        raise NotImplementedError
