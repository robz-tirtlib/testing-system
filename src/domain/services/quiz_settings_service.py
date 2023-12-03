from abc import ABC, abstractmethod
from uuid import uuid4
from src.domain.models.new_types import QuizId

from src.domain.models.quiz import (
    Quiz, QuizSettingsFull, QuizSettingsIn, QuizSettingsUpdate,
)

from src.domain.repos.quiz import IQuizRepo


class IQuizSettingsService(ABC):
    @abstractmethod
    def parse_input_settings_on_creation(
        self, quiz_settings_in: QuizSettingsIn
    ) -> QuizSettingsFull:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_settings(self, quiz_id: QuizId) -> QuizSettingsFull:
        raise NotImplementedError

    @abstractmethod
    def update_quiz_settings(
        self, quiz: Quiz, quiz_settings: QuizSettingsUpdate,
    ) -> QuizSettingsFull:
        raise NotImplementedError


class QuizSettingsService(IQuizSettingsService):
    def __init__(self, quiz_repo: IQuizRepo) -> None:
        self.quiz_repo = quiz_repo

    def get_quiz_settings(self, quiz_id: QuizId) -> QuizSettingsFull:
        quiz = self.quiz_repo.get_quiz_by_id(quiz_id)

        if quiz is None:
            raise Exception("Quiz with id={quiz_id} does not exist.")

        return QuizSettingsFull(
            time_limit=quiz.time_limit,
            private=False if quiz.private_link is None else quiz.private_link,
            is_active=quiz.is_active,
        )

    def update_quiz_settings(
            self, quiz: Quiz, settings_update: QuizSettingsUpdate,
    ) -> QuizSettingsFull:
        quiz_settings_full = self._get_full_settings_from_settings_update(
            quiz, settings_update,
        )

        self.quiz_repo.update_quiz_settings(quiz.id, quiz_settings_full)

        return quiz_settings_full

    def _get_full_settings_from_settings_update(
            self, quiz: Quiz, settings_update: QuizSettingsUpdate,
    ) -> QuizSettingsFull:
        quiz_settings_full = QuizSettingsFull(
            time_limit=quiz.time_limit,
            private=True if quiz.private_link is not None else False,
            private_link=quiz.private_link,
        )

        if settings_update.private is not None:
            if settings_update.private is False:
                quiz_settings_full.private = False
                quiz_settings_full.private_link = None
            if settings_update.private is True and quiz.private_link is None:
                quiz_settings_full.private_link = self._generate_private_link()
                quiz_settings_full.private = True

        if settings_update.time_limit is not None:
            quiz_settings_full.time_limit = settings_update.time_limit

        return quiz_settings_full

    def _generate_private_link(self) -> str:
        return str(uuid4())
