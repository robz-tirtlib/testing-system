import datetime

from src.domain.models.new_types import UserId, TestPassId
from src.domain.models.test import Test
from src.domain.models.test_pass import (
    TestPassCreate, TestPass, TestPassOwnerDetails,
)
from src.domain.models.question import QuestionWithUserAnswers, Question
from src.domain.models.answer import UserAnswer, Answer

from src.domain.repos.test import ITestRepo, ITestPassRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo


class TestPassService:
    def start_test_pass(
            self, test_pass: TestPassCreate, test_pass_repo: ITestPassRepo,
    ) -> TestPass:
        return test_pass_repo.create_test_pass(test_pass)

    def get_details(
            self, test_pass_id: TestPassId, user_id: UserId,
            test_repo: ITestRepo, test_pass_repo: ITestPassRepo,
            answer_repo: IAnswerRepo, question_repo: IQuestionRepo,
    ) -> None:
        test_pass = test_pass_repo.get_test_pass_by_id(test_pass_id)
        test = test_repo.get_test_by_id(test_pass.test_id)

        if test_pass is None or test is None:
            return  # TODO: raise custom exception

        if user_id == test.creator_id:
            return self._details_for_owner(
                test, user_id, test_pass, question_repo, answer_repo,
            )

        if user_id == test_pass.user_id:
            return self._details_for_user()

        # TODO: custom access Exception
        raise Exception("You do not have access to these details.")

    def _details_for_owner(
            self, test: Test, user_id: UserId, test_pass: TestPass,
            question_repo: IQuestionRepo, answer_repo: IAnswerRepo,
    ) -> TestPassOwnerDetails:
        questions_with_user_answers = self._get_questions_with_user_answers(
            question_repo, test, answer_repo, test_pass, user_id,
        )

        # TODO: Allow not limited tests
        time_delta = datetime.timedelta(seconds=test.time_limit)
        test_ending = test_pass.started_at + time_delta
        is_finished = True if test_ending <= datetime.datetime.now() else False
        test_pass_owner_details = TestPassOwnerDetails(
            test_id=test.id,
            test_pass_id=test_pass.id,
            user_id=user_id,
            started_at=test_pass.started_at,
            is_finished=is_finished,
            questions=questions_with_user_answers,
        )

        return test_pass_owner_details

    def _get_questions_with_user_answers(
            self, question_repo: IQuestionRepo, test: Test,
            answer_repo: IAnswerRepo, test_pass: TestPass,
            user_id: UserId,
    ) -> list[QuestionWithUserAnswers]:
        questions_with_user_answers: list[QuestionWithUserAnswers] = []

        for question in question_repo.get_questions_by_test_id(test.id):
            question_with_user_answers = self._get_question_with_user_answers(
                answer_repo, question, test_pass, user_id, test,
            )
            questions_with_user_answers.append(question_with_user_answers)

        return questions_with_user_answers

    def _get_question_with_user_answers(
            self, answer_repo: IAnswerRepo, question: Question,
            test_pass: TestPass, user_id: UserId, test: Test,
    ) -> QuestionWithUserAnswers:
        answers = answer_repo.get_answers_by_question_id(question.id)
        user_answers = answer_repo.get_user_answers(
            test_pass_id=test_pass.id,
            question_id=question.id,
            user_id=user_id,
        )

        is_correct = self._is_user_correct(answers, user_answers)

        question_with_user_answers = QuestionWithUserAnswers(
            id=question.id,
            test_id=test.id,
            text=question.text,
            question_type=question.question_type,
            answers=answers,
            user_answers=user_answers,
            is_correct=is_correct,
        )

        return question_with_user_answers

    def _is_user_correct(
            self, answers: list[Answer], user_answers: list[UserAnswer]
    ) -> bool:
        # TODO: Check for no_choice questions

        is_correct = True
        for answer in answers:
            if answer.is_correct is False:
                continue

            found = False
            for user_answer in user_answers:
                if user_answer.answer_id == answer.id:
                    found = True
            if found is False:
                is_correct = False

        return is_correct

    def _details_for_user(self):
        return
