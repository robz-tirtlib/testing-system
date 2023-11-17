from src.domain.models.test_pass import TestPassCreate, TestPass
from src.domain.models.new_types import UserId, TestPassId

from src.domain.repos.test import ITestPassRepo


class TestPassService:
    def start_test_pass(
            self, test_pass: TestPassCreate, test_pass_repo: ITestPassRepo,
    ) -> TestPass:
        return test_pass_repo.create_test_pass(test_pass)

    def get_details(
            self, test_pass_id: TestPassId, user_id: UserId,
            test_owner_id: UserId, test_pass_repo: ITestPassRepo,
    ) -> None:
        test_pass = test_pass_repo.get_test_pass_by_id(test_pass_id)

        if test_pass is None:
            return

        if user_id == test_owner_id:
            return self.get_owner_details()

        if user_id == test_pass.user_id:
            return self.get_user_details()

        # TODO: custom access Exception
        raise Exception("You do not have access to these details.")

    def get_owner_details(self):
        return

    def get_user_details(self):
        return
