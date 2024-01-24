from dataclasses import dataclass

from src.domain.models.new_types import QuizId

from src.domain.models.quiz import QuizDataForUser

from src.domain.services.quiz_pass_service import QuizPassService
from src.domain.services.quiz_service import QuizAggregateService, QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class StartQuizPass:
    quiz_id: QuizId
    accessed_via_private_link: bool


class StartQuizPassHandler:

    def __init__(
            self, quiz_service: QuizService,
            quiz_pass_service: QuizPassService,
            quiz_settings_service: QuizSettingsService,
            quiz_aggregate_service: QuizAggregateService,
    ) -> None:
        self._quiz_service = quiz_service
        self._quiz_pass_service = quiz_pass_service
        self._quiz_settings_service = quiz_settings_service
        self._quiz_aggregate_service = quiz_aggregate_service

    def __call__(self, command: StartQuizPass) -> QuizDataForUser:
        quiz_settings = self._quiz_settings_service.get_quiz_settings(
            command.quiz_id)

        if not quiz_settings.is_active:
            raise Exception

        if quiz_settings.private != command.accessed_via_private_link:
            raise Exception

        quiz_w_questions = self._quiz_aggregate_service.get_quiz_for_user(
            command.quiz_id)

        quiz = QuizDataForUser(
            quiz_settings=quiz_settings,
            quiz=quiz_w_questions,
        )

        return quiz
