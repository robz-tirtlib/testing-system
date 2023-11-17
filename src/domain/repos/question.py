from abc import ABC, abstractmethod

from src.domain.models.new_types import QuestionId, TestId
from src.domain.models.question import Question, QuestionCreate


class IQuestionRepo(ABC):
    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        raise NotImplementedError

    @abstractmethod
    def get_questions_by_test_id(
        self, test_id: TestId,
    ) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def create_questions(
        self, questions: list[QuestionCreate]
    ) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def create_question(self, question: QuestionCreate) -> Question:
        raise NotImplementedError
