from src.domain.models.new_types import (
    UserId, QuestionId, QuizId,
)
from src.domain.models.quiz import (
    Quiz, QuizSettingsIn, QuizSettingsFull, QuizDataForOwner,
    QuizWQuestionsAndAnswers, QuizWQuestions, QuizDataForUser,
    QuizSettingsUpdate,
)
from src.domain.models.question import (
    Question, QuestionCreate, QuestionWithCorrectAnswersCreate,
    QuestionWithCorrectAnswers, QuestionWithAnswers
    )
from src.domain.models.answer import Answer, AnswerCreate

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo

from uuid import uuid4

from src.domain.services.quiz_settings_service import IQuizSettingsService

# TODO: delete/edit Quiz questions, Question answers


class QuizService:
    def __init__(self, quiz_repo: IQuizRepo) -> None:
        self.quiz_repo = quiz_repo

    def add_quiz(
            self, quiz_settings_service: IQuizSettingsService,
            question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo, quiz_settings_in: QuizSettingsIn,
            questions: list[QuestionWithCorrectAnswersCreate], user_id: UserId,
    ) -> Quiz:
        quiz_settings = quiz_settings_service.parse_input_settings_on_creation(
            quiz_settings_in,
        )
        created_quiz = self.quiz_repo.create_quiz(quiz_settings, user_id)

        for question_with_answers in questions:
            self._add_question_with_answers(
                question_repo, answer_repo, created_quiz,
                question_with_answers,
            )

        return created_quiz

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

    def set_quiz_active(self, quiz_id: QuizId, quiz_repo: IQuizRepo) -> None:
        if not quiz_repo.update_is_active(quiz_id, True):
            raise Exception(f"There is no quiz with id={quiz_id}.")

    def set_quiz_inactive(self, quiz_id: QuizId, quiz_repo: IQuizRepo) -> None:
        if not quiz_repo.update_is_active(quiz_id, False):
            raise Exception(f"There is no quiz with id={quiz_id}.")

    def update_quiz_settings(
            self, quiz_id: QuizId, settings_update: QuizSettingsUpdate,
            quiz_settings_service: IQuizSettingsService, user_id: UserId,
    ) -> QuizSettingsFull:
        quiz = self.quiz_repo.get_quiz_by_id(quiz_id)

        if quiz is None:
            raise Exception("Quiz does not exist.")

        if quiz.creator_id != user_id:
            raise Exception("You do not have access to editing this quiz.")

        quiz_settings_full = quiz_settings_service.update_quiz_settings(
            quiz, settings_update,
        )
        return quiz_settings_full

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

    def _add_question_with_answers(
            self, question_repo: IQuestionRepo, answer_repo: IAnswerRepo,
            created_quiz: Quiz,
            question_with_answers: QuestionWithCorrectAnswersCreate,
    ) -> None:
        question_create = QuestionCreate(
            quiz_id=created_quiz.id,
            text=question_with_answers.text,
            question_type=question_with_answers.question_type,
        )
        created_question = self.add_question(
            question_repo, question_create,
            )
        self.add_answers(
            answer_repo, question_with_answers.answers,
            created_question.id,
            )

    def add_questions(
            self, question_repo: IQuestionRepo,
            questions: list[QuestionCreate],
    ) -> list[Question]:
        return question_repo.create_questions(questions)

    def add_question(
            self, question_repo: IQuestionRepo, question: QuestionCreate,
    ) -> Question:
        return question_repo.create_question(question)

    def add_answers(
            self, answer_repo: IAnswerRepo,
            answers: list[AnswerCreate], question_id: QuestionId,
    ) -> list[Answer]:
        return answer_repo.create_answers(answers, question_id)

    def _generate_private_link(self) -> str:
        return str(uuid4())
