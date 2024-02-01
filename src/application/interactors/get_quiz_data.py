from dataclasses import dataclass

from src.application.common.interactor import Interactor

from src.domain.dto.quiz import QuizDataForOwner

from src.domain.models.new_types import QuizId, UserId

from src.domain.services.quiz_service import QuizAggregateService, QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class GetQuizDataDTO:
    quiz_id: QuizId
    user_id: UserId


class GetQuizData(Interactor[GetQuizDataDTO, QuizDataForOwner]):
    def __init__(
            self, quiz_service: QuizService,
            quiz_aggregate_service: QuizAggregateService,
            quiz_settings_service: QuizSettingsService,
    ) -> None:
        self._quiz_service = quiz_service
        self._quiz_aggregate_service = quiz_aggregate_service
        self._quiz_settings_service = quiz_settings_service

    def __call__(self, data: GetQuizDataDTO) -> QuizDataForOwner:
        owner_id = self._quiz_service.get_owner_id(data.quiz_id)

        if owner_id != data.user_id:
            raise Exception("No access.")

        quiz = self._quiz_aggregate_service.get_quiz_for_owner(data.quiz_id)
        quiz_settings = self._quiz_settings_service.get_quiz_settings(
            data.quiz_id)

        quiz_data = QuizDataForOwner(
            quiz_settings=quiz_settings,
            quiz=quiz,
        )

        return quiz_data
