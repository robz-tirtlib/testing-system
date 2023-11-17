import pytest
import datetime

from unittest.mock import Mock

from src.domain.repos.test import ITestRepo, ITestPassRepo

from src.domain.models.new_types import TestPassId
from src.domain.models.test import TestSettingsFull
from src.domain.models.test_pass import TestPass, TestPassCreate

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


def test_no_access_throws_exception(
        test_pass_service: TestPassService, test_pass_repo: ITestPassRepo,
        test_repo: ITestRepo,
):
    user_id, test_id = 1, 1
    test_pass_create = TestPassCreate(user_id=user_id, test_id=test_id)
    test_pass = test_pass_service.start_test_pass(
        test_pass_create, test_pass_repo,
    )

    test_repo.create_test(
        test_settings=TestSettingsFull(
            time_limit=100,
            private_link=None,
            private=False,
        ),
        user_id=3,
    )

    with pytest.raises(Exception):
        test_pass_service.get_details(
            test_pass.id, 2, test_repo, test_pass_repo,
        )
