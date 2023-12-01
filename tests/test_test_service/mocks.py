import datetime

from src.domain.models.new_types import (
    UserId, TestId, QuestionId, AnswerId, TestPassId,
)

from src.domain.models.test import Test, TestSettingsFull
from src.domain.models.question import Question, QuestionCreate
from src.domain.models.answer import Answer, AnswerCreate, UserAnswer

from src.domain.repos.test import ITestRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo


class TestRepoMock(ITestRepo):
    def __init__(self) -> None:
        self.tests: dict[int, Test] = {}
        self._test_id = 1

    def get_test_by_id(self, test_id: TestId) -> Test | None:
        return self.tests.get(test_id, None)

    def create_test(
            self, test_settings: TestSettingsFull,
            user_id: UserId
    ) -> Test:
        test = Test(
            id=self._test_id,
            creator_id=user_id,
            private_link=test_settings.private_link,
            time_limit=test_settings.time_limit,
            created_at=datetime.datetime.now(),
        )
        self.tests[1] = test

        self._test_id += 1
        return test

    def update_is_active(
            self, test_id: TestId, change_to_active: bool
    ) -> None:
        test = self.tests.get(test_id, None)

        if test is None:
            return False

        if change_to_active:
            test.is_active = True
        else:
            test.is_active = False
        return True

    def update_test_settings(
            self, test_id: TestId, test_settings: TestSettingsFull
    ) -> None:
        test = self.tests.get(test_id)
        test.time_limit = test_settings.time_limit
        test.private_link = test_settings.private_link
        test.is_active = test_settings.is_active


class QuestionRepoMock(IQuestionRepo):
    def __init__(self) -> None:
        self.questions: dict[int, Question] = {}
        self._question_id = 1

    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        return self.questions.get(question_id, None)

    def get_questions_by_test_id(
        self, test_id: TestId,
    ) -> list[Question]:
        questions = []

        for _, question in self.questions.items():
            if question.test_id == test_id:
                questions.append(question)

        return questions

    def create_questions(
        self, questions: list[QuestionCreate],
    ) -> list[Question]:
        created_questions = []

        for question in questions:
            created_question = Question(
                id=self._question_id,
                test_id=question.test_id,
                text=question.text,
                question_type=question.question_type,
            )
            self.questions[self._question_id] = created_question
            created_questions.append(created_question)

            self._question_id += 1
        return created_questions

    def create_question(self, question: QuestionCreate) -> Question:
        created_question = Question(
                id=self._question_id,
                test_id=question.test_id,
                text=question.text,
                question_type=question.question_type,
            )
        self.questions[self._question_id] = created_question
        self._question_id += 1

        return created_question


class AnswerRepoMock(IAnswerRepo):
    def __init__(self) -> None:
        self.answers: dict[int, Answer] = {}
        self._answer_id = 1

    def get_answer_by_id(self, answer_id: AnswerId) -> Answer | None:
        return self.answers.get(answer_id, None)

    def get_answers_by_question_id(
        self, question_id: QuestionId
    ) -> list[Answer]:
        answers = []

        for _, answer in self.answers.items():
            if answer.question_id == question_id:
                answers.append(answer)

        return answers

    def get_user_answers(
        self, test_pass_id: TestPassId, question_id: QuestionId,
        user_id: UserId,
    ) -> list[UserAnswer]:
        raise NotImplementedError

    def create_answers(
        self, answers: list[AnswerCreate], question_id: QuestionId,
    ) -> list[Answer]:
        created_answers = []

        for answer in answers:
            created_answer = Answer(
                id=self._answer_id,
                question_id=question_id,
                text=answer.text,
                is_correct=answer.is_correct,
            )
            self.answers[self._answer_id] = created_answer
            created_answers.append(created_answer)
            self._answer_id += 1

        return created_answers

    def create_user_answers(
        self, test_pass_id: TestPassId, question_id: QuestionId,
        answer_id: AnswerId, user_id: UserId,
    ) -> UserAnswer:
        raise NotImplementedError
