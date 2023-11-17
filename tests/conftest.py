import pytest

from tests.test_test_service.mocks import (
    TestRepoMock, QuestionRepoMock, AnswerRepoMock,
)

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
