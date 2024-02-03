from src.domain.exceptions.base import DomainError


class TooManyAnswersError(DomainError):
    def __init__(self, question_id) -> None:
        self._question_id = question_id

    def __str__(self):
        return f"Too many answers on question with id={self._question_id}"
