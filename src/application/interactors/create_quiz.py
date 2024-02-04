from dataclasses import dataclass

from src.application.common.interactor import Interactor

from src.domain.dto.question import QuestionWithAnswersCreate
from src.domain.dto.quiz import QuizSettingsIn

from src.domain.models.new_types import QuizId, UserId

from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.services.question_service import QuestionService
from src.domain.services.quiz_service import QuizService
from src.domain.services.quiz_settings_service import QuizSettingsService


@dataclass
class CreateQuizDTO:
    user_id: UserId
    title: str
    quiz_settings: QuizSettingsIn
    questions: list[QuestionWithAnswersCreate]


class CreateQuiz(Interactor[CreateQuizDTO, QuizId]):
    def __init__(
            self,
            quiz_service: QuizService,
            quiz_settings_service: QuizSettingsService,
            question_service: QuestionService,
            question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ) -> QuizId:
        self._quiz_service = quiz_service
        self._quiz_settings_service = quiz_settings_service
        self._question_service = question_service
        self._question_repo = question_repo
        self._answer_repo = answer_repo

    def __call__(self, data: CreateQuizDTO) -> QuizId:
        quiz_settings = self._quiz_settings_service.parse_input_settings(
            data.quiz_settings,
        )
        quiz = self._quiz_service.add_quiz(
            quiz_settings, data.user_id, data.title,
        )

        for question in data.questions:
            question_create = self._question_service.create_question(
                quiz.id, question.text, question.question_type,
            )
            created_question = self._question_repo.create_question(
                question_create, quiz.id,
            )
            self._question_service.validate_answers(
                created_question, question.answers,
            )
            self._answer_repo.create_answers(
                answers=question.answers,
                question_id=created_question.id,
            )

        return quiz.id
