from abc import ABC, abstractmethod

from src.domain.models.question import QuestionId, Question, QuestionCreate


class IQuestionRepo(ABC):
    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Question:
        raise NotImplementedError

    @abstractmethod
    def create_questions(
        self, questions: list[QuestionCreate]
    ) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def create_question(self, question: QuestionCreate) -> Question:
        raise NotImplementedError
