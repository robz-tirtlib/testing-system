from src.domain.exceptions.base import DomainError


class QuizPassError(DomainError):
    def __init__(self, quiz_pass_id):
        self._quiz_pass_id = quiz_pass_id


class QuizPassNotFound(QuizPassError):
    def __str__(self) -> str:
        return f"Quiz pass with id={self._quiz_pass_id} does not exist."


class TimeOutError(QuizPassError):
    def __str__(self) -> str:
        return f"Quiz pass with id={self._quiz_pass_id} timed out."
