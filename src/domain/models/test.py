from dataclasses import dataclass
from datetime import datetime

from .new_types import TestId
from .user import UserId
from .question import QuestionWithAnswers


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


# TODO: TestWQuestions
@dataclass
class TestFullData:
    id: TestId
    creator_id: UserId
    private_link: str | None
    time_limit: int
    created_at: datetime
    questions: list[QuestionWithAnswers]


@dataclass
class TestFullOwner:
    test_settings: TestSettingsFull
    test: TestFullData
