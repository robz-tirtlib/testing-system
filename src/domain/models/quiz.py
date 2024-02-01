from dataclasses import dataclass

from .new_types import QuizId, UserId


@dataclass
class Quiz:
    id: QuizId
    creator_id: UserId
    title: str


@dataclass
class QuizSettings:
    time_limit: int | None
    private: bool
    private_link: str | None
    is_active: bool = True
