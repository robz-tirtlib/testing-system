from dataclasses import dataclass
from enum import Enum

from .new_types import QuestionId
from .quiz import QuizId


class QuestionType(Enum):
    no_choice = 0
    single_choice = 1
    multi_choice = 2

    @classmethod
    def has(cls, value) -> bool:
        return value in [member.value for member in cls]


@dataclass
class Question:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType
