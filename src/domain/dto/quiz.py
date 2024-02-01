from dataclasses import dataclass
from datetime import datetime

from src.domain.dto.question import (
    QuestionWithCorrectAnswers, QuestionWithPossibleAnswers,
)

from src.domain.models.new_types import QuizId, UserId
from src.domain.models.question import Question
from src.domain.models.quiz import Quiz, QuizSettings


@dataclass
class QuizSettingsIn:
    time_limit: int | None
    private: bool
    is_active: bool = True


@dataclass
class QuizSettingsUpdate:
    time_limit: int | None = None
    private: bool | None = None
    is_active: bool | None = None


@dataclass
class QuizWQuestionsAndAnswers:
    id: QuizId
    creator_id: UserId
    private_link: str | None
    time_limit: int | None
    created_at: datetime
    questions: list[QuestionWithCorrectAnswers]


@dataclass
class QuizWQuestions:
    id: QuizId
    creator_id: UserId
    title: str
    questions: list[Question]


@dataclass
class QuizForUser(Quiz):
    questions: list[QuestionWithPossibleAnswers]


@dataclass
class QuizForOwner(Quiz):
    questions: list[QuestionWithCorrectAnswers]


@dataclass
class QuizDataForOwner:
    quiz_settings: QuizSettings
    quiz: QuizForOwner


@dataclass
class QuizDataForUser:
    quiz_settings: QuizSettings
    quiz: QuizForUser
