from dataclasses import dataclass
from enum import Enum

from .new_types import QuestionId
from .test import TestId
from .answer import Answer, UserAnswer, AnswerCreate


class QuestionType(Enum):
    no_choice = 0
    single_choice = 1
    multi_choice = 2


@dataclass
class Question:
    id: QuestionId
    test_id: TestId
    text: str
    question_type: QuestionType


@dataclass
class QuestionCreate:
    test_id: TestId
    text: str
    question_type: QuestionType


@dataclass
class QuestionWithCorrectAnswersCreate:
    text: str
    question_type: QuestionType
    answers: list[AnswerCreate]


@dataclass
class QuestionWithCorrectAnswers:
    id: QuestionId
    test_id: TestId
    text: str
    question_type: QuestionType
    answers: list[Answer]


@dataclass
class QuestionWithUserAnswers:
    id: QuestionId
    test_id: TestId
    text: str
    question_type: QuestionType
    user_answers: list[UserAnswer]


@dataclass
class QuestionWithAllAnswers:
    id: QuestionId
    test_id: TestId
    text: str
    question_type: QuestionType
    answers: list[Answer]
    user_answers: list[UserAnswer]
    is_correct: bool
