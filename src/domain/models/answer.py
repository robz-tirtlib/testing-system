from dataclasses import dataclass
from datetime import datetime

from .new_types import AnswerId, UserAnswerId, QuestionId, QuizPassId, UserId


@dataclass
class Answer:
    id: AnswerId
    question_id: QuestionId
    text: str
    is_correct: bool


@dataclass
class PossibleAnswer:
    id: AnswerId
    question_id: QuestionId
    text: str


@dataclass
class AnswerCreate:
    text: str
    is_correct: bool


# TODO: remake UserAnswer to stor list of answers for question
@dataclass
class UserAnswer:
    id: UserAnswerId
    quiz_pass_id: QuizPassId
    question_id: QuestionId
    user_id: UserId
    answer_id: AnswerId | None
    created_at: datetime
    is_correct: bool
