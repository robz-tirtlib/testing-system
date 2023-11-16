from dataclasses import dataclass
from typing import NewType
from datetime import datetime

from .question import QuestionId
from .test import TestPassId


AnswerId = NewType("AnswerId", int)
UserAnswerId = NewType("UserAnswerId", int)


@dataclass
class Answer:
    id: AnswerId
    question_id: QuestionId
    text: str
    is_correct: bool


@dataclass
class AnswerCreate:
    question_id: QuestionId
    text: str
    is_correct: bool


@dataclass
class UserAnswer:
    id: UserAnswerId
    test_pass_id: TestPassId
    question_id: QuestionId
    answer_id: AnswerId
    created_at: datetime
