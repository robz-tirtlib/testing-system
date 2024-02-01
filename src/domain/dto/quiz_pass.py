from dataclasses import dataclass
from datetime import datetime
from src.domain.dto.question import QuestionWithAllAnswers

from src.domain.models.new_types import (
    AnswerId, QuestionId, QuizId, QuizPassId, UserId,
)
from src.domain.models.question import QuestionType


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


@dataclass
class UserAnswersIn:
    question_id: QuestionId
    question_type: QuestionType
    choice_answers: list[AnswerId] | None
    no_choice_answer: str | None


@dataclass
class StopQuizPassDTO:
    quiz_pass_id: QuizPassId
    user_id: UserId
    user_answers: list[UserAnswersIn]
    stoppage_time: datetime
