from abc import ABC, abstractmethod

from src.domain.models.new_types import TestId, UserId, TestPassId
from src.domain.models.test import Test, TestSettingsFull

from src.domain.models.test_pass import TestPass, TestPassCreate


class ITestRepo(ABC):
    @abstractmethod
    def get_test_by_id(self, test_id: TestId) -> Test | None:
        raise NotImplementedError

    @abstractmethod
    def create_test(
        self, test_settings: TestSettingsFull, user_id: UserId,
    ) -> Test:
        raise NotImplementedError

    @abstractmethod
    def update_is_active(
        self, test_id: TestId, change_to_active: bool
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_test_settings(
        self, test_id: TestId, test_settings: TestSettingsFull,
    ) -> None:
        raise NotImplementedError


class ITestPassRepo(ABC):
    @abstractmethod
    def get_test_pass_by_id(self, test_pass_id: TestPassId) -> TestPass | None:
        raise NotImplementedError

    @abstractmethod
    def create_test_pass(self, test_pass: TestPassCreate) -> TestPass:
        raise NotImplementedError

    @abstractmethod
    def finish_test_pass(self, test_pass_id: TestPassId) -> None:
        raise NotImplementedError
