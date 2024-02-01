from dataclasses import dataclass

from src.domain.models.new_types import AnswerId, QuestionId


@dataclass
class PossibleAnswer:
    id: AnswerId
    question_id: QuestionId
    text: str


@dataclass
class AnswerCreate:
    text: str
    is_correct: bool
