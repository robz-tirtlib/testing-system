from abc import ABC, abstractmethod

from src.domain.models.test import (
    TestId, Test, TestSettingsFull,
    TestPassId, TestPass, TestPassCreate,
    )


class ITestRepo(ABC):
    @abstractmethod
    def get_test_by_id(self, test_id: TestId) -> Test | None:
        raise NotImplementedError

    @abstractmethod
    def create_test(self, test_settings: TestSettingsFull) -> Test:
        raise NotImplementedError


class ITestPassRepo(ABC):
    @abstractmethod
    def get_test_pass_by_id(self, test_pass_id: TestPassId) -> TestPass | None:
        raise NotImplementedError

    @abstractmethod
    def create_test_pass(self, test_pass: TestPassCreate) -> TestPass:
        raise NotImplementedError
