import pytest
import datetime

from unittest.mock import Mock, MagicMock

from src.domain.repos.test import ITestPassRepo

from src.domain.models.new_types import TestPassId
from src.domain.models.test import Test
from src.domain.models.test_pass import (
    TestPass, TestPassCreate, TestPassOwnerDetails,
)
from src.domain.models.question import Question, QuestionType
from src.domain.models.answer import Answer, UserAnswer

from src.domain.services.test_pass_service import TestPassService


@pytest.fixture
def test_pass_service() -> TestPassService:
    _test_pass_service = TestPassService()
    yield _test_pass_service


class TestPassRepoMock(ITestPassRepo):
    def __init__(self) -> None:
        self.test_passes: dict[int, TestPass] = {}
        self._test_pass_id = 1

    def get_test_pass_by_id(self, test_pass_id: TestPassId) -> TestPass | None:
        return self.test_passes.get(test_pass_id, None)

    def create_test_pass(self, test_pass: TestPassCreate) -> TestPass:
        created_test_pass = TestPass(
            id=self._test_pass_id,
            user_id=test_pass.user_id,
            test_id=test_pass.test_id,
            started_at=datetime.datetime.now(),
            is_finished=False,
        )
        self.test_passes[self._test_pass_id] = created_test_pass

        self._test_pass_id += 1
        return created_test_pass

    def finish_test_pass(self, test_pass_id: TestPassId) -> None:
        test_pass = self.test_passes.get(test_pass_id, None)

        if test_pass is None:
            return

        test_pass.is_finished = True


@pytest.fixture
def test_pass_repo() -> ITestPassRepo:
    _test_pass_repo = TestPassRepoMock()
    yield _test_pass_repo


def test_test_pass_creation(
        test_pass_service: TestPassService, test_pass_repo: ITestPassRepo,
):
    user_id, test_id = 1, 1
    test_pass_create = TestPassCreate(user_id=user_id, test_id=test_id)
    test_pass = test_pass_service.start_test_pass(
        test_pass_create, test_pass_repo,
    )
    assert test_pass is not None
    assert test_pass.test_id == 1


def test_no_access_throws_exception(test_pass_service: TestPassService):
    user_id, test_id, test_pass_id = 1, 1, 1

    test_pass_repo_mock = Mock()
    test_pass_repo_mock.get_test_pass_by_id = MagicMock(
        return_value=TestPass(
            id=1,
            user_id=user_id,
            test_id=test_id,
            started_at=datetime.datetime.now(),
            is_finished=False,
        )
    )

    assert test_pass_repo_mock.get_test_pass_by_id().id == 1

    test_repo_mock = Mock()
    test_repo_mock.get_test_by_id = MagicMock(
        return_value=Test(
            id=test_id,
            creator_id=user_id,
            private_link=None,
            time_limit=100,
            created_at=datetime.datetime.now(),
        )
    )

    assert test_repo_mock.get_test_by_id().id == 1

    with pytest.raises(Exception):
        test_pass_service.get_details(
            test_pass_id, 2, test_repo_mock, test_pass_repo_mock,
        )


def test_details_for_owner(test_pass_service: TestPassService):
    user_id, test_id, test_pass_id = 1, 1, 1
    test_repo = Mock()
    test = Test(
        id=test_id,
        creator_id=user_id,
        private_link=None,
        time_limit=100,
        created_at=datetime.datetime.now(),
    )
    test_repo.get_test_by_id = MagicMock(
        return_value=test,
    )
    assert test_repo.get_test_by_id().id == test_id

    test_pass_repo = Mock()
    test_pass = TestPass(
        id=test_pass_id,
        user_id=user_id,
        test_id=test_id,
        started_at=datetime.datetime.now(),
        is_finished=False,
    )
    test_pass_repo.get_test_pass_by_id = MagicMock(
        return_value=test_pass,
    )
    assert test_pass_repo.get_test_pass_by_id().test_id == test_id

    question_repo = Mock()
    questions = [
        Question(
            id=1,
            test_id=test_id,
            text="Question",
            question_type=QuestionType.single_choice,
        ),
    ]
    question_repo.get_questions_by_test_id = MagicMock(
        return_value=questions,
    )
    assert len(question_repo.get_questions_by_test_id()) == 1

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
            test_pass_id=test_pass_id,
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

    owner_details: TestPassOwnerDetails = test_pass_service.get_details(
        test_pass_id, user_id, test_repo, test_pass_repo, answer_repo,
        question_repo,
    )
    assert len(owner_details.questions) == 1
    assert owner_details.questions[0].is_correct is False

    user_answers = [
        UserAnswer(
            id=1,
            test_pass_id=test_pass_id,
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

    owner_details: TestPassOwnerDetails = test_pass_service.get_details(
        test_pass_id, user_id, test_repo, test_pass_repo, answer_repo,
        question_repo,
    )
    assert len(owner_details.questions) == 1
    assert owner_details.questions[0].is_correct is True
