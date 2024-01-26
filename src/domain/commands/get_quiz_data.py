from dataclasses import dataclass

from src.domain.models.new_types import QuizId, UserId
from src.domain.models.quiz import QuizDataForOwner
from src.domain.services.quiz_service import QuizAggregateService, QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class QuizDataCommand:
    quiz_id: QuizId
    user_id: UserId


class GetQuizData:
    def __init__(
            self, quiz_service: QuizService,
            quiz_aggregate_service: QuizAggregateService,
            quiz_settings_service: QuizSettingsService,
    ) -> None:
        self._quiz_service = quiz_service
        self._quiz_aggregate_service = quiz_aggregate_service
        self._quiz_settings_service = quiz_settings_service

    def __call__(self, command: QuizDataCommand) -> QuizDataForOwner:
        owner_id = self._quiz_service.get_owner_id(command.quiz_id)

        if owner_id != command.user_id:
            raise Exception("No access.")

        quiz = self._quiz_aggregate_service.get_quiz_for_owner(command.quiz_id)
        quiz_settings = self._quiz_settings_service.get_quiz_settings(
            command.quiz_id)

        quiz_data = QuizDataForOwner(
            quiz_settings=quiz_settings,
            quiz=quiz,
        )

        return quiz_data
