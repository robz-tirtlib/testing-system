import pytest

from tests.test_quiz_service.mocks import (
    QuizRepoMock, QuestionRepoMock, AnswerRepoMock,
)

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.services.quiz_service import QuizService


@pytest.fixture
def quiz_repo() -> IQuizRepo:
    _quiz_repo = QuizRepoMock()
    yield _quiz_repo


@pytest.fixture
def quiz_service(quiz_repo: IQuizRepo) -> QuizService:
    _quiz_service = QuizService(quiz_repo)
    yield _quiz_service


@pytest.fixture
def question_repo() -> IQuestionRepo:
    _question_repo = QuestionRepoMock()
    yield _question_repo


@pytest.fixture
def answer_repo() -> IQuestionRepo:
    _answer_repo = AnswerRepoMock()
    yield _answer_repo
