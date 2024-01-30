from datetime import datetime

from dataclasses import dataclass

from src.application.common.interactor import Interactor

from src.domain.models.new_types import (
    AnswerId, QuestionId, QuizPassId, UserId,
)
from src.domain.models.question import QuestionType
from src.domain.services.quiz_pass_service import (
    QuizPassService, QuizPassUserService,
)
from src.domain.services.quiz_settings_service import QuizSettingsService


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


class StopQuizPass(Interactor[Interactor, None]):
    def __init__(
            self, quiz_pass_service: QuizPassService,
            quiz_settings_service: QuizSettingsService,
            quiz_pass_user_service: QuizPassUserService,
    ) -> None:
        self._quiz_pass_service = quiz_pass_service
        self._quiz_settings_service = quiz_settings_service
        self._quiz_pass_user_service = quiz_pass_user_service

    def __call__(self, data: StopQuizPassDTO) -> None:
        quiz_id = self._quiz_pass_service.get_quiz_id(data.quiz_pass_id)
        quiz_settings = self._quiz_settings_service.get_quiz_settings(quiz_id)
        self._quiz_pass_service.stop_quiz_pass(
            data.quiz_pass_id, data.user_id, data.stoppage_time,
            quiz_settings.time_limit,
        )

        self._quiz_pass_user_service.write_answers(data)
