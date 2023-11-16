from dataclasses import dataclass
from typing import NewType
from datetime import datetime

from .user import UserId


TestId = NewType("TestId", int)
TestPassId = NewType("TestPassId", int)


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
