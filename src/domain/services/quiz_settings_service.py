from abc import ABC, abstractmethod
from uuid import uuid4
from src.domain.models.new_types import QuizId

from src.domain.dto.quiz import QuizSettingsIn, QuizSettingsUpdate

from src.domain.models.quiz import QuizSettings

from src.domain.repos.quiz import IQuizRepo


class IQuizSettingsService(ABC):
    @abstractmethod
    def parse_input_settings(
        self, quiz_settings_in: QuizSettingsIn
    ) -> QuizSettings:
        raise NotImplementedError

    @abstractmethod
    def generate_private_link(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_settings(self, quiz_id: QuizId) -> QuizSettings:
        raise NotImplementedError

    @abstractmethod
    def update_quiz_settings(
        self, quiz_id: QuizId, settings_update: QuizSettingsUpdate,
    ) -> QuizSettings:
        raise NotImplementedError


class QuizSettingsService(IQuizSettingsService):
    def __init__(self, quiz_repo: IQuizRepo) -> None:
        self._quiz_repo = quiz_repo

    def parse_input_settings(
        self, quiz_settings_in: QuizSettingsIn
    ) -> QuizSettings:
        private_link = None

        if quiz_settings_in.private:
            private_link = self.generate_private_link()

        quiz_settings = QuizSettings(
            time_limit=quiz_settings_in.time_limit,
            private=quiz_settings_in.private,
            private_link=private_link,
        )

        return quiz_settings

    def get_quiz_settings(self, quiz_id: QuizId) -> QuizSettings:
        return self._quiz_repo.get_quiz_settings(quiz_id)

    def update_quiz_settings(
            self, quiz_id: QuizId, settings_update: QuizSettingsUpdate,
    ) -> QuizSettings:
        """
        Should be check if user is permitted to do this operation
        (PermissionService)
        """
        quiz_settings = self._quiz_repo.get_quiz_settings(quiz_id)
        quiz_settings_full = self._get_full_settings_from_settings_update(
            quiz_settings, settings_update,
        )

        self._quiz_repo.update_quiz_settings(quiz_id, quiz_settings_full)

        return quiz_settings_full

    def _get_full_settings_from_settings_update(
            self, quiz: QuizSettings, settings_update: QuizSettingsUpdate,
    ) -> QuizSettings:
        quiz_settings_full = QuizSettings(
            time_limit=quiz.time_limit,
            private=True if quiz.private_link is not None else False,
            private_link=quiz.private_link,
        )

        if settings_update.private is not None:
            if settings_update.private is False:
                quiz_settings_full.private = False
                quiz_settings_full.private_link = None
            if settings_update.private is True and quiz.private_link is None:
                quiz_settings_full.private_link = self.generate_private_link()
                quiz_settings_full.private = True

        if settings_update.time_limit is not None:
            quiz_settings_full.time_limit = settings_update.time_limit

        if settings_update.is_active is not None:
            quiz_settings_full.is_active = settings_update.is_active

        return quiz_settings_full

    def generate_private_link(self) -> str:
        return str(uuid4())
