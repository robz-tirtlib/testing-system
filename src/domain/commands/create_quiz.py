from dataclasses import dataclass

from src.domain.models.new_types import QuizId, UserId
from src.domain.models.question import QuestionWithAnswersCreate
from src.domain.models.quiz import QuizSettingsIn
from src.domain.services.question_service import QuestionService
from src.domain.services.quiz_service import QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class CreateQuizCommand:
    user_id: UserId
    title: str
    quiz_settings: QuizSettingsIn
    questions: list[QuestionWithAnswersCreate]


class CreateQuiz:
    def __init__(
            self,
            quiz_service: QuizService,
            quiz_settings_service: QuizSettingsService,
            question_service: QuestionService,
    ) -> None:
        self._quiz_service = quiz_service
        self._quiz_settings_service = quiz_settings_service
        self._question_service = question_service

    def __call__(self, command: CreateQuizCommand) -> QuizId:
        quiz_settings = self._quiz_settings_service.parse_input_settings(
            command.quiz_settings,
        )
        quiz = self._quiz_service.add_quiz(
            quiz_settings, command.user_id, command.title,
        )
        self._question_service.add_questions_with_answers(
            command.questions, quiz.id,
        )

        return quiz.id
