from dataclasses import dataclass
from datetime import datetime

from .new_types import QuizPassId
from .quiz import QuizId
from .user import UserId
from .question import QuestionWithAllAnswers


@dataclass
class QuizPass:
    id: QuizPassId
    user_id: UserId
    quiz_id: QuizId
    started_at: datetime
    is_finished: bool


@dataclass
class QuizPassCreate:
    user_id: UserId
    quiz_id: QuizId


@dataclass
class QuizPassOwnerDetails:
    quiz_id: QuizId
    quiz_pass_id: QuizPassId
    user_id: UserId
    started_at: datetime
    is_finished: bool
    questions: list[QuestionWithAllAnswers]


@dataclass
class QuizPassUserDetails:
    quiz_id: QuizId
    quiz_pass_id: QuizPassId
    user_id: UserId
    started_at: datetime
    is_finished: bool
    questions: list[int]


@dataclass
class QuizPassResult:
    quiz_pass_id: QuizPassId
    correct_answers: int
    wrong_answers: int
