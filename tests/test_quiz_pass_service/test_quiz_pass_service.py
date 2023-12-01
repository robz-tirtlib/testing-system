import pytest
import datetime

from unittest.mock import Mock, MagicMock

from src.domain.repos.quiz import IQuizPassRepo

from src.domain.models.new_types import QuizPassId
from src.domain.models.quiz import Quiz
from src.domain.models.quiz_pass import (
    QuizPass, QuizPassCreate, QuizPassOwnerDetails,
)
from src.domain.models.question import Question, QuestionType
from src.domain.models.answer import Answer, UserAnswer

from src.domain.services.quiz_pass_service import QuizPassService


@pytest.fixture
def quiz_pass_service() -> QuizPassService:
    _quiz_pass_service = QuizPassService()
    yield _quiz_pass_service


class QuizPassRepoMock(IQuizPassRepo):
    def __init__(self) -> None:
        self.quiz_passes: dict[int, QuizPass] = {}
        self._quiz_pass_id = 1

    def get_quiz_pass_by_id(self, quiz_pass_id: QuizPassId) -> QuizPass | None:
        return self.quiz_passes.get(quiz_pass_id, None)

    def create_quiz_pass(self, quiz_pass: QuizPassCreate) -> QuizPass:
        created_quiz_pass = QuizPass(
            id=self._quiz_pass_id,
            user_id=quiz_pass.user_id,
            quiz_id=quiz_pass.quiz_id,
            started_at=datetime.datetime.now(),
            is_finished=False,
        )
        self.quiz_passes[self._quiz_pass_id] = created_quiz_pass

        self._quiz_pass_id += 1
        return created_quiz_pass

    def finish_quiz_pass(self, quiz_pass_id: QuizPassId) -> None:
        quiz_pass = self.quiz_passes.get(quiz_pass_id, None)

        if quiz_pass is None:
            return

        quiz_pass.is_finished = True


@pytest.fixture
def quiz_pass_repo() -> IQuizPassRepo:
    _quiz_pass_repo = QuizPassRepoMock()
    yield _quiz_pass_repo


def test_quiz_pass_creation(
        quiz_pass_service: QuizPassService, quiz_pass_repo: IQuizPassRepo,
):
    user_id, quiz_id = 1, 1
    quiz_pass_create = QuizPassCreate(user_id=user_id, quiz_id=quiz_id)
    quiz_pass = quiz_pass_service.start_quiz_pass(
        quiz_pass_create, quiz_pass_repo,
    )
    assert quiz_pass is not None
    assert quiz_pass.quiz_id == 1


def test_no_access_throws_exception(quiz_pass_service: QuizPassService):
    user_id, quiz_id, quiz_pass_id = 1, 1, 1

    quiz_pass_repo_mock = Mock()
    quiz_pass_repo_mock.get_quiz_pass_by_id = MagicMock(
        return_value=QuizPass(
            id=1,
            user_id=user_id,
            quiz_id=quiz_id,
            started_at=datetime.datetime.now(),
            is_finished=False,
        )
    )

    assert quiz_pass_repo_mock.get_quiz_pass_by_id().id == 1

    quiz_repo_mock = Mock()
    quiz_repo_mock.get_quiz_by_id = MagicMock(
        return_value=Quiz(
            id=quiz_id,
            creator_id=user_id,
            private_link=None,
            time_limit=100,
            created_at=datetime.datetime.now(),
        )
    )

    assert quiz_repo_mock.get_quiz_by_id().id == 1

    with pytest.raises(Exception):
        quiz_pass_service.get_details(
            quiz_pass_id, 2, quiz_repo_mock, quiz_pass_repo_mock,
        )


def test_details_for_owner(quiz_pass_service: QuizPassService):
    user_id, quiz_id, quiz_pass_id = 1, 1, 1
    quiz_repo = Mock()
    quiz = Quiz(
        id=quiz_id,
        creator_id=user_id,
        private_link=None,
        time_limit=100,
        created_at=datetime.datetime.now(),
    )
    quiz_repo.get_quiz_by_id = MagicMock(
        return_value=quiz,
    )
    assert quiz_repo.get_quiz_by_id().id == quiz_id

    quiz_pass_repo = Mock()
    quiz_pass = QuizPass(
        id=quiz_pass_id,
        user_id=user_id,
        quiz_id=quiz_id,
        started_at=datetime.datetime.now(),
        is_finished=False,
    )
    quiz_pass_repo.get_quiz_pass_by_id = MagicMock(
        return_value=quiz_pass,
    )
    assert quiz_pass_repo.get_quiz_pass_by_id().quiz_id == quiz_id

    question_repo = Mock()
    questions = [
        Question(
            id=1,
            quiz_id=quiz_id,
            text="Question",
            question_type=QuestionType.single_choice,
        ),
    ]
    question_repo.get_questions_by_quiz_id = MagicMock(
        return_value=questions,
    )
    assert len(question_repo.get_questions_by_quiz_id()) == 1

    answer_repo = Mock()
    answers = [
        Answer(
            id=1,
            question_id=1,
            text="Answer",
            is_correct=True,
        ),
        Answer(
            id=2,
            question_id=1,
            text="Answer",
            is_correct=False,
        ),
    ]
    answer_repo.get_answers_by_question_id = MagicMock(
        return_value=answers,
    )
    assert len(answer_repo.get_answers_by_question_id()) == 2

    user_answers = [
        UserAnswer(
            id=1,
            quiz_pass_id=quiz_pass_id,
            question_id=1,
            user_id=user_id,
            answer_id=2,
            created_at=datetime.datetime.now(),
            is_correct=False,
        ),
    ]
    answer_repo.get_user_answers = MagicMock(
        return_value=user_answers,
    )
    assert len(answer_repo.get_user_answers()) == 1

    owner_details: QuizPassOwnerDetails = quiz_pass_service.get_details(
        quiz_pass_id, user_id, quiz_repo, quiz_pass_repo, answer_repo,
        question_repo,
    )
    assert len(owner_details.questions) == 1
    assert owner_details.questions[0].is_correct is False

    user_answers = [
        UserAnswer(
            id=1,
            quiz_pass_id=quiz_pass_id,
            question_id=1,
            user_id=user_id,
            answer_id=1,
            created_at=datetime.datetime.now(),
            is_correct=True,
        ),
    ]
    answer_repo.get_user_answers = MagicMock(
        return_value=user_answers,
    )
    assert len(answer_repo.get_user_answers()) == 1

    owner_details: QuizPassOwnerDetails = quiz_pass_service.get_details(
        quiz_pass_id, user_id, quiz_repo, quiz_pass_repo, answer_repo,
        question_repo,
    )
    assert len(owner_details.questions) == 1
    assert owner_details.questions[0].is_correct is True
