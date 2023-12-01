from src.domain.models.new_types import (
    UserId, QuestionId, TestId,
)
from src.domain.models.test import (
    Test, TestSettingsIn, TestSettingsFull, TestDataForOwner,
    TestWQuestionsAndAnswers, TestWQuestions, TestDataForUser,
)
from src.domain.models.question import (
    Question, QuestionCreate, QuestionWithCorrectAnswersCreate,
    QuestionWithCorrectAnswers,
    )
from src.domain.models.answer import Answer, AnswerCreate

from src.domain.repos.test import ITestRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo

from uuid import uuid4

# TODO: delete Test/ edit Test settings
# TODO: delete/edit Test questions, Question answers


class TestService:
    def add_test(
            self, test_repo: ITestRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo, test_settings_in: TestSettingsIn,
            questions: list[QuestionWithCorrectAnswersCreate], user_id: UserId,
    ) -> Test:
        test_settings = self._get_settings(test_settings_in)
        created_test = test_repo.create_test(test_settings, user_id)

        for question_with_answers in questions:
            self._add_question_with_answers(
                question_repo, answer_repo, created_test,
                question_with_answers,
            )

        return created_test

    def get_test(
            self, test_repo: ITestRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo, test_id: TestId, user_id: UserId,
            accessed_via_private_link: bool,
    ) -> TestDataForUser | TestDataForOwner:
        # TODO: separate get_test for owner and user (user sees only settings
        # questions and possible answers, but owner also sees correct answers)
        test = test_repo.get_test_by_id(test_id)

        if test is None:
            # TODO: custom exception
            raise Exception("Test does not exist.")

        if test.private_link is not None and not accessed_via_private_link:
            raise Exception("Test could only be accessed via private link.")

        if test.creator_id == user_id:
            return self._get_test_for_owner(test, question_repo, answer_repo)

        if not test.is_active:
            raise Exception("Could not access inactive test.")
        return self._get_test_for_user(test, question_repo)

    def set_test_active(self, test_id: TestId, test_repo: ITestRepo) -> None:
        if not test_repo.update_is_active(test_id, True):
            raise Exception(f"There is no test with id={test_id}.")

    def set_test_inactive(self, test_id: TestId, test_repo: ITestRepo) -> None:
        if not test_repo.update_is_active(test_id, False):
            raise Exception(f"There is no test with id={test_id}.")

    def _get_test_for_owner(
            self, test: Test, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ):
        test_settings = TestSettingsFull(
            time_limit=test.time_limit,
            private_link=test.private_link,
            private=(True if test.private_link else False),
            is_active=test.is_active,
        )

        questions = question_repo.get_questions_by_test_id(test_id=test.id)
        questions_with_answers = []

        for question in questions:
            answers = answer_repo.get_answers_by_question_id(
                question_id=question.id)
            question_with_answers = QuestionWithCorrectAnswers(
                id=question.id,
                test_id=test.id,
                text=question.text,
                question_type=question.question_type,
                answers=answers,
            )
            questions_with_answers.append(question_with_answers)

        test_with_questions = TestWQuestionsAndAnswers(
            id=test.id,
            creator_id=test.creator_id,
            private_link=test.private_link,
            time_limit=test.time_limit,
            created_at=test.created_at,
            questions=questions_with_answers,
        )

        test_data_for_owner = TestDataForOwner(
            test_settings=test_settings,
            test=test_with_questions,
        )

        return test_data_for_owner

    def _get_test_for_user(
            self, test: Test, question_repo: IQuestionRepo,
    ):
        test_settings = TestSettingsFull(
            time_limit=test.time_limit,
            private_link=test.private_link,
            private=(True if test.private_link else False),
            is_active=test.is_active,
        )

        # TODO: pass possible answers if exist to user
        questions = question_repo.get_questions_by_test_id(test_id=test.id)
        test_with_questions = TestWQuestions(
            id=test.id,
            creator_id=test.creator_id,
            private_link=test.private_link,
            time_limit=test.time_limit,
            created_at=test.created_at,
            questions=questions,
        )

        test_data_for_user = TestDataForUser(
            test_settings=test_settings,
            test=test_with_questions,
        )

        return test_data_for_user

    def _get_settings(self, test_settings: TestSettingsIn) -> TestSettingsFull:
        private_link = None
        if test_settings.private:
            private_link = self._generate_private_link()

        return TestSettingsFull(
            time_limit=test_settings.time_limit,
            private=test_settings.private,
            private_link=private_link,
        )

    def _add_question_with_answers(
            self, question_repo: IQuestionRepo, answer_repo: IAnswerRepo,
            created_test: Test,
            question_with_answers: QuestionWithCorrectAnswersCreate,
    ) -> None:
        question_create = QuestionCreate(
            test_id=created_test.id,
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
