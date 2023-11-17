from dataclasses import dataclass
from datetime import datetime

from .new_types import TestPassId
from .test import TestId
from .user import UserId
from .question import QuestionWithUserAnswers


@dataclass
class TestPass:
    id: TestPassId
    user_id: UserId
    test_id: TestId
    started_at: datetime
    is_finished: bool


@dataclass
class TestPassCreate:
    user_id: UserId
    test_id: TestId


@dataclass
class TestPassOwnerDetails:
    id: TestPassId
    user_id: UserId
    test_id: TestId
    started_at: datetime
    is_finished: bool
    questions: list[QuestionWithUserAnswers]
