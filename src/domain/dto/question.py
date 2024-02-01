from dataclasses import dataclass

from src.domain.dto.answer import AnswerCreate, PossibleAnswer

from src.domain.models.answer import Answer, UserAnswer
from src.domain.models.new_types import QuestionId, QuizId
from src.domain.models.question import QuestionType


@dataclass
class QuestionCreate:
    quiz_id: QuizId
    text: str
    question_type: QuestionType


@dataclass
class QuestionWithAnswersCreate:
    text: str
    question_type: QuestionType
    answers: list[AnswerCreate]


@dataclass
class QuestionWithPossibleAnswers:
    id: QuestionId
    quiz_id: QuizId
    text: str
    question_type: QuestionType
    possible_answers: list[PossibleAnswer]


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
