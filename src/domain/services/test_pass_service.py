from src.domain.models.test import TestPassId, TestPassCreate, TestPass

from src.domain.repos.test import ITestPassRepo


class TestPassService:
    def start_test_pass(
            self, test_pass: TestPassCreate, test_pass_repo: ITestPassRepo,
    ) -> TestPass:
        return test_pass_repo.create_test_pass(test_pass)

    def get_test_pass_details(
            self, test_pass_id: TestPassId,
    ) -> None:
        return
