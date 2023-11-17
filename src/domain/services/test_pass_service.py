from src.domain.models.test_pass import TestPassCreate, TestPass
from src.domain.models.new_types import UserId, TestPassId

from src.domain.repos.test import ITestRepo, ITestPassRepo


class TestPassService:
    def start_test_pass(
            self, test_pass: TestPassCreate, test_pass_repo: ITestPassRepo,
    ) -> TestPass:
        return test_pass_repo.create_test_pass(test_pass)

    def get_details(
            self, test_pass_id: TestPassId, user_id: UserId,
            test_repo: ITestRepo, test_pass_repo: ITestPassRepo,
    ) -> None:
        test_pass = test_pass_repo.get_test_pass_by_id(test_pass_id)
        test = test_repo.get_test_by_id(test_pass.test_id)

        if test_pass is None or test is None:
            return  # TODO: raise custom exception

        if user_id == test.creator_id:
            return self._details_for_owner()

        if user_id == test_pass.user_id:
            return self._details_for_user()

        # TODO: custom access Exception
        raise Exception("You do not have access to these details.")

    def _details_for_owner(self):
        return

    def _details_for_user(self):
        return
