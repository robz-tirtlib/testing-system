from dataclasses import dataclass
from datetime import datetime

from .new_types import TestId, UserId
from .question import QuestionWithAnswers, Question


@dataclass
class Test:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int
    created_at: datetime


@dataclass
class TestSettingsIn:
    time_limit: int
    private: bool


@dataclass
class TestSettingsFull:
    time_limit: int
    private: bool
    private_link: str | None


@dataclass
class TestWQuestionsAndAnswers:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int
    created_at: datetime
    questions: list[QuestionWithAnswers]


@dataclass
class TestWQuestions:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int
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
