from dataclasses import dataclass

from src.domain.models.new_types import QuizPassId, UserId
from src.domain.models.quiz_pass import QuizPassResult
from src.domain.services.quiz_pass_result_service import QuizPassResultService
from src.domain.services.quiz_pass_service import QuizPassService
from src.domain.services.quiz_service import QuizService


@dataclass
class QuizPassResultCommand:
    user_id: UserId
    quiz_pass_id: QuizPassId


class QuizPassResultHandler:
    def __init__(
            self, quiz_pass_result_service: QuizPassResultService,
            quiz_pass_service: QuizPassService,
            quiz_service: QuizService,
    ) -> None:
        self._quiz_pass_result_service = quiz_pass_result_service
        self._quiz_pass_service = quiz_pass_service
        self._quiz_service = quiz_service

    def __call__(self, command: QuizPassResultCommand) -> QuizPassResult:
        quiz_id = self._quiz_pass_service.get_quiz_id(command.quiz_pass_id)
        owner_id = self._quiz_service.get_owner_id(quiz_id)
        user_id = self._quiz_pass_service.get_user_id(command.quiz_pass_id)

        if command.user_id not in [user_id, owner_id]:
            raise Exception("Not allowed to view this quiz pass.")

        result = self._quiz_pass_result_service.get_quiz_pass_result(
            command.quiz_pass_id,
        )

        if result is not None:
            return result

        result = self._quiz_pass_result_service.calc_quiz_pass_result(
            command.quiz_pass_id,
        )

        return result
