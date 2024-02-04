from src.domain.exceptions.base import DomainError


class TooManyAnswersError(DomainError):
    def __init__(self, question_id) -> None:
        self._question_id = question_id

    def __str__(self):
        return f"Too many answers on question with id={self._question_id}"


class TooFewAnswersError(DomainError):
    def __init__(self, question_id) -> None:
        self._question_id = question_id

    def __str__(self):
        return f"Too few answers on question with id={self._question_id}"


class QuestionTypeError(DomainError):
    def __init__(self, question_type) -> None:
        self._question_type = question_type
    def __str__(self):
        return f"Provided question type ({self._question_type}) does not exist."
