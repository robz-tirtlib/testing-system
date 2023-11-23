from dataclasses import dataclass
from datetime import datetime

from .new_types import TestId, UserId
from .question import QuestionWithCorrectAnswers, Question


@dataclass
class Test:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int | None
    created_at: datetime


@dataclass
class TestSettingsIn:
    time_limit: int | None
    private: bool


@dataclass
class TestSettingsFull:
    time_limit: int | None
    private: bool
    private_link: str | None


@dataclass
class TestWQuestionsAndAnswers:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int | None
    created_at: datetime
    questions: list[QuestionWithCorrectAnswers]


@dataclass
class TestWQuestions:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int | None
    created_at: datetime
    questions: list[Question]


@dataclass
class TestDataForOwner:
    test_settings: TestSettingsFull
    test: TestWQuestionsAndAnswers


@dataclass
class TestDataForUser:
    test_settings: TestSettingsFull
    test: TestWQuestions
