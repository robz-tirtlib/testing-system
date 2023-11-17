import pytest

from tests.test_test_service.mocks import (
    TestRepoMock, QuestionRepoMock, AnswerRepoMock,
)


from src.domain.models.test import TestSettingsIn
from src.domain.models.question import (
    QuestionWithAnswersCreate, QuestionType,
)
from src.domain.models.answer import AnswerCreate

from src.domain.repos.test import ITestRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.services.test_service import TestService


@pytest.fixture
def test_service() -> TestService:
    _test_service = TestService()
    yield _test_service


@pytest.fixture
def test_repo() -> ITestRepo:
    _test_repo = TestRepoMock()
    yield _test_repo


@pytest.fixture
def question_repo() -> IQuestionRepo:
    _question_repo = QuestionRepoMock()
    yield _question_repo


@pytest.fixture
def answer_repo() -> IQuestionRepo:
    _answer_repo = AnswerRepoMock()
    yield _answer_repo


def test_test_creation(
        test_repo: TestRepoMock, question_repo: QuestionRepoMock,
        answer_repo: AnswerRepoMock, test_service: TestService,
):
    test_settings_in = TestSettingsIn(time_limit=0, private=False)
    user_id = 2
    questions = [
        QuestionWithAnswersCreate(
            text="What's good?",
            question_type=QuestionType.single_choice,
            answers=[
                AnswerCreate("Fine", True),
                AnswerCreate("Bad", False),
            ]
        ),
        QuestionWithAnswersCreate(
            text="If x * x = 4. Which value could x be?",
            question_type=QuestionType.single_choice,
            answers=[
                AnswerCreate("2", True),
                AnswerCreate("-2", True),
                AnswerCreate("-2", False),
            ]
        )
    ]
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )
    assert test is not None
    assert test.id == 1
    assert test.creator_id == 2
    assert test.private_link is None
    assert test.time_limit == 0

    test_full_data = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, user_id,
    )

    assert test_full_data is not None
    assert len(test_full_data.test.questions) == len(questions)
    assert (
        test_full_data.test_settings.time_limit == test_settings_in.time_limit)
