from dataclasses import dataclass
from datetime import datetime

from .new_types import QuizId, UserId
from .question import QuestionWithCorrectAnswers, Question


@dataclass
class Quiz:
    id: QuizId
    creator_id: UserId
    private_link: str | None
    time_limit: int | None
    created_at: datetime
    is_active: bool = True


@dataclass
class QuizSettingsIn:
    time_limit: int | None
    private: bool
    is_active: bool = True


@dataclass
class QuizSettingsUpdate:
    time_limit: int | None = None
    private: bool | None = None


@dataclass
class QuizSettingsFull:
    time_limit: int | None
    private: bool
    private_link: str | None
    is_active: bool = True


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
    private_link: str | None
    time_limit: int | None
    created_at: datetime
    questions: list[Question]


@dataclass
class QuizDataForOwner:
    quiz_settings: QuizSettingsFull
    quiz: QuizWQuestionsAndAnswers


@dataclass
class QuizDataForUser:
    quiz_settings: QuizSettingsFull
    quiz: QuizWQuestions
