from dataclasses import dataclass

from .new_types import AnswerId, UserAnswerId, QuestionId, QuizPassId


@dataclass
class Answer:
    id: AnswerId
    question_id: QuestionId
    text: str
    is_correct: bool


@dataclass
class PossibleAnswer:
    id: AnswerId
    question_id: QuestionId
    text: str


@dataclass
class AnswerCreate:
    text: str
    is_correct: bool


@dataclass
class UserAnswer:
    user_answer_id: UserAnswerId
    question_id: QuestionId
    quiz_pass_id: QuizPassId
    choice_answer: list[AnswerId] | None
    no_choice_answer: str | None
