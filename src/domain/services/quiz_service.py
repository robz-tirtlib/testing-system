from src.domain.models.new_types import UserId, QuizId
from src.domain.models.quiz import (
    Quiz, QuizSettingsIn, QuizSettingsFull, QuizDataForOwner,
    QuizWQuestionsAndAnswers, QuizWQuestions, QuizDataForUser,
)
from src.domain.models.question import (
    QuestionWithCorrectAnswers, QuestionWithAnswers
)

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo

from uuid import uuid4
from src.domain.services.permission_service import IPermissionService
from src.domain.services.question_service import IQuestionService

from src.domain.services.quiz_settings_service import IQuizSettingsService


class QuizService:
    def __init__(self, quiz_repo: IQuizRepo) -> None:
        self.quiz_repo = quiz_repo

    def add_quiz(
            self, quiz_settings_service: IQuizSettingsService,
            quiz_settings_in: QuizSettingsIn, user_id: UserId,
    ) -> Quiz:
        quiz_settings = quiz_settings_service.parse_input_settings_on_creation(
            quiz_settings_in,
        )
        created_quiz = self.quiz_repo.create_quiz(quiz_settings, user_id)

        return created_quiz

    def get_quiz_for_user():
        pass

    def get_quiz_for_owner(
            self, question_service: IQuestionService, quiz_id: QuizId,
            permission_service: IPermissionService,
    ) -> QuizDataForOwner:
        quiz = self.quiz_repo.get_quiz_by_id(quiz_id)

        if quiz is None:
            raise Exception("Quiz does not exist.")

    def get_quiz(
            self, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo, quiz_id: QuizId, user_id: UserId,
            accessed_via_private_link: bool,
    ) -> QuizDataForUser | QuizDataForOwner:
        # TODO: separate get_quiz for owner and user (user sees only settings
        # questions and possible answers, but owner also sees correct answers)
        quiz = self.quiz_repo.get_quiz_by_id(quiz_id)

        if quiz is None:
            # TODO: custom exception
            raise Exception("Quiz does not exist.")

        if quiz.private_link is not None and not accessed_via_private_link:
            raise Exception("Quiz could only be accessed via private link.")

        if quiz.creator_id == user_id:
            return self._get_quiz_for_owner(quiz, question_repo, answer_repo)

        if not quiz.is_active:
            raise Exception("Could not access inactive quiz.")
        return self._get_quiz_for_user(quiz, question_repo, answer_repo)

    def _get_quiz_for_owner(
            self, quiz: Quiz, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ):
        quiz_settings = self._get_settings_from_quiz(quiz)

        questions = question_repo.get_questions_by_quiz_id(quiz_id=quiz.id)
        questions_with_answers = []

        for question in questions:
            answers = answer_repo.get_answers_by_question_id(
                question_id=question.id)
            question_with_answers = QuestionWithCorrectAnswers(
                id=question.id,
                quiz_id=quiz.id,
                text=question.text,
                question_type=question.question_type,
                answers=answers,
            )
            questions_with_answers.append(question_with_answers)

        quiz_with_questions = QuizWQuestionsAndAnswers(
            id=quiz.id,
            creator_id=quiz.creator_id,
            private_link=quiz.private_link,
            time_limit=quiz.time_limit,
            created_at=quiz.created_at,
            questions=questions_with_answers,
        )

        quiz_data_for_owner = QuizDataForOwner(
            quiz_settings=quiz_settings,
            quiz=quiz_with_questions,
        )

        return quiz_data_for_owner

    def _get_quiz_for_user(
            self, quiz: Quiz, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ):
        quiz_settings = self._get_settings_from_quiz(quiz)

        questions = question_repo.get_questions_by_quiz_id(quiz_id=quiz.id)

        questions_with_answers = []

        for question in questions:
            answers = answer_repo.get_answers_by_question_id(question.id)
            question_with_answers = QuestionWithAnswers(
                id=question.id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
                answers=answers,
            )
            questions_with_answers.append(question_with_answers)

        quiz_with_questions = QuizWQuestions(
            id=quiz.id,
            creator_id=quiz.creator_id,
            private_link=quiz.private_link,
            time_limit=quiz.time_limit,
            created_at=quiz.created_at,
            questions=questions_with_answers,
        )

        quiz_data_for_user = QuizDataForUser(
            quiz_settings=quiz_settings,
            quiz=quiz_with_questions,
        )

        return quiz_data_for_user

    def _get_full_settings_on_creation(
            self, quiz_settings: QuizSettingsIn,
    ) -> QuizSettingsFull:
        private_link = None
        if quiz_settings.private:
            private_link = self._generate_private_link()

        return QuizSettingsFull(
            time_limit=quiz_settings.time_limit,
            private=quiz_settings.private,
            private_link=private_link,
        )

    def _get_settings_from_quiz(self, quiz: Quiz) -> QuizSettingsFull:
        return QuizSettingsFull(
            time_limit=quiz.time_limit,
            private_link=quiz.private_link,
            private=(True if quiz.private_link else False),
            is_active=quiz.is_active,
        )

    def _generate_private_link(self) -> str:
        return str(uuid4())


class QuizAggregateService:

    def __init__(
            self, quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ) -> None:
        self._quiz_repo = quiz_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo

    def get_quiz_for_user(self, quiz_id: QuizId) -> QuizWQuestions:
        quiz = self._quiz_repo.get_quiz_by_id(quiz_id)
        questions = self._question_repo.get_questions_by_quiz_id(quiz_id=quiz.id)

        questions_with_answers = []

        for question in questions:
            answers = self._answer_repo.get_answers_by_question_id(question.id)
            question_with_answers = QuestionWithAnswers(
                id=question.id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
                answers=answers,
            )
            questions_with_answers.append(question_with_answers)

        quiz_with_questions = QuizWQuestions(
            id=quiz.id,
            creator_id=quiz.creator_id,
            title=quiz.title,
            questions=questions_with_answers,
        )

        return quiz_with_questions
