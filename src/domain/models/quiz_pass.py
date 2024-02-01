from dataclasses import dataclass
from datetime import datetime

from .new_types import QuizPassId
from .quiz import QuizId
from .user import UserId


@dataclass
class QuizPass:
    id: QuizPassId
    user_id: UserId
    quiz_id: QuizId
    started_at: datetime
    is_finished: bool
