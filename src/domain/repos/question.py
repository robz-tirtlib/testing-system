from abc import ABC, abstractmethod

from src.domain.models.new_types import QuestionId, QuizId
from src.domain.models.question import Question, QuestionCreate


class IQuestionRepo(ABC):
    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        raise NotImplementedError

    @abstractmethod
    def get_questions_by_quiz_id(
        self, quiz_id: QuizId,
    ) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def create_questions(
        self, questions: list[QuestionCreate], quiz_id: QuizId,
    ) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def create_question(
        self, question: QuestionCreate, quiz_id: QuizId
    ) -> Question:
        raise NotImplementedError
