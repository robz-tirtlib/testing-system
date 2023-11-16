from src.domain.models.test import Test, TestSettingsIn, TestSettingsFull
from src.domain.models.question import Question, QuestionCreate
from src.domain.models.answer import Answer, AnswerCreate

from src.domain.repos.test import ITestRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo

from uuid import uuid4


class TestService:
    def create_test(
            self, test_repo: ITestRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo, test_settings: TestSettingsIn,
            questions: list[QuestionCreate], answers: list[AnswerCreate],
    ) -> Test:
        private_link = None
        if test_settings.private:
            private_link = self._generate_private_link()

        test_settings_full = TestSettingsFull(
            time_limit=test_settings.time_limit,
            private=test_settings.private,
            private_link=private_link,
        )
        test = test_repo.create_test(test_settings_full)

        self.add_questions(question_repo, questions)
        self.add_answers(answer_repo, answers)

        return test

    def add_questions(
            self, question_repo: IQuestionRepo,
            questions: list[QuestionCreate],
    ) -> list[Question]:
        return question_repo.create_questions(questions)

    def add_question(
            self, question_repo: IQuestionRepo, question: QuestionCreate
    ) -> Question:
        return question_repo.create_question(question)

    def add_answers(
            self, answer_repo: IAnswerRepo,
            answers: list[AnswerCreate]
    ) -> list[Answer]:
        return answer_repo.create_answers(answers)

    def _generate_private_link(self) -> str:
        return str(uuid4())
