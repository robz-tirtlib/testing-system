from dataclasses import dataclass

from src.domain.models.new_types import QuizId, UserId

from src.domain.models.quiz import QuizDataForUser
from src.domain.models.quiz_pass import QuizPass, QuizPassCreate

from src.domain.services.quiz_pass_service import QuizPassService
from src.domain.services.quiz_service import QuizAggregateService, QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class StartQuizPass:
    quiz_id: QuizId | None
    accessed_via_private_link: bool
    private_link: str
    user_id: UserId


@dataclass
class StartedQuizPassData:
    quiz_data: QuizDataForUser
    quiz_pass_data: QuizPass


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

    def __call__(self, command: StartQuizPass) -> StartedQuizPassData:
        if command.accessed_via_private_link:
            quiz_id = self._quiz_service.get_quiz_by_link(command.private_link)
        else:
            quiz_id = command.quiz_id

        quiz_settings = self._quiz_settings_service.get_quiz_settings(quiz_id)

        if not quiz_settings.is_active:
            raise Exception

        if quiz_settings.private != command.accessed_via_private_link:
            raise Exception

        quiz_w_questions = self._quiz_aggregate_service.get_quiz_for_user(
            command.quiz_id)

        quiz_data = QuizDataForUser(
            quiz_settings=quiz_settings,
            quiz=quiz_w_questions,
        )

        quiz_pass_data = self._quiz_pass_service.start_quiz_pass(
            QuizPassCreate(
                quiz_id=quiz_w_questions.id,
                user_id=command.user_id,
            ))

        started_quiz_pass_data = StartedQuizPassData(
            quiz_data=quiz_data,
            quiz_pass_data=quiz_pass_data,
        )
        return started_quiz_pass_data
