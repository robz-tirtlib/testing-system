from src.domain.exceptions.base import DomainError


class QuizError(DomainError):
    def __init__(self, quiz_id = None, private_link = None):
        self._quiz_id = quiz_id
        self._private_link = private_link


class QuizNotFound(QuizError):
    def __str__(self) -> str:
        if self._private_link:
            return f"Quiz with link={self._private_link} does not exist."
        return f"Quiz with id={self._quiz_id} does not exist."
