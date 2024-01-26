from src.domain.models.answer import PossibleAnswer
from src.domain.models.new_types import UserId, QuizId
from src.domain.models.quiz import (
    Quiz, QuizForOwner, QuizForUser, QuizSettingsIn, QuizWQuestions,
)
from src.domain.models.question import (
    QuestionWithAnswers, QuestionWithPossibleAnswers,
)

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo

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

    def get_quiz_by_link(self, private_link: str) -> Quiz:
        quiz = self.quiz_repo.get_quiz_by_link(private_link)

        if quiz is None:
            raise Exception

        return quiz

    def get_owner_id(self, quiz_id: QuizId) -> UserId | None:
        owner_id = self.quiz_repo.get_owner_id(quiz_id)

        if owner_id is None:
            raise Exception(f"No quiz with {quiz_id=}")

        return owner_id


class QuizAggregateService:

    def __init__(
            self, quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ) -> None:
        self._quiz_repo = quiz_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo

    def get_quiz_for_user(
            self, quiz_id: QuizId,
    ) -> QuizForUser:
        quiz = self._get_quiz(quiz_id)

        for i, question in enumerate(quiz.questions):
            for j, answer in enumerate(question.answers):
                question.answers[j] = PossibleAnswer(
                    id=answer.id,
                    question_id=answer.question_id,
                    text=answer.text,
                )
            quiz.questions[i] = QuestionWithPossibleAnswers(
                id=question.id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
                possible_answers=question.answers,
            )

        return quiz

    def get_quiz_for_owner(
            self, quiz_id: QuizId,
    ) -> QuizForOwner:
        return self._get_quiz(quiz_id)

    def _get_quiz(self, quiz_id: QuizId) -> QuizForOwner:
        quiz = self._quiz_repo.get_quiz_by_id(quiz_id)
        questions = self._question_repo.get_questions_by_quiz_id(
            quiz_id=quiz.id)

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
