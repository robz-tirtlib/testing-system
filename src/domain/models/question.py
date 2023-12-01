from dataclasses import dataclass
from enum import Enum

from .new_types import QuestionId
from .quiz import QuizId
from .answer import Answer, UserAnswer, AnswerCreate


class QuestionType(Enum):
    no_choice = 0
    single_choice = 1
    multi_choice = 2


@dataclass
class Question:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType


@dataclass
class QuestionCreate:
    quiz_id: QuizId
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
    quiz_id: QuizId
    text: str
    question_type: QuestionType
    answers: list[Answer]


@dataclass
class QuestionWithUserAnswers:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType
    user_answers: list[UserAnswer]


@dataclass
class QuestionWithAllAnswers:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType
    answers: list[Answer]
    user_answers: list[UserAnswer]
    is_correct: bool


@dataclass
class QuestionWithAnswers:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType
    answers: list[Answer]
