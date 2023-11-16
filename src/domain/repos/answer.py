from abc import ABC, abstractmethod

from src.domain.models.answer import AnswerId, Answer, AnswerCreate


class IAnswerRepo(ABC):
    @abstractmethod
    def get_answer_by_id(self, answer_id: AnswerId) -> Answer:
        raise NotImplementedError

    @abstractmethod
    def create_answers(
        self, answers: list[AnswerCreate]
    ) -> list[Answer]:
        raise NotImplementedError
