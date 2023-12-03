import pytest

import datetime

from unittest.mock import Mock, MagicMock
from src.domain.models.quiz import Quiz, QuizSettingsUpdate
from src.domain.repos.quiz import IQuizRepo

from src.domain.services.quiz_settings_service import (
    IQuizSettingsService, QuizSettingsService,
)


@pytest.fixture
def quiz_repo() -> IQuizRepo:
    _quiz_repo = Mock()
    yield _quiz_repo


@pytest.fixture
def quiz_settings_service(quiz_repo: IQuizRepo) -> IQuizSettingsService:
    _quiz_settings_service = QuizSettingsService(quiz_repo)
    yield _quiz_settings_service


def test_get_non_existent_quiz_settings(
        quiz_settings_service: IQuizSettingsService
):
    quiz_settings_service.quiz_repo.get_quiz_by_id = MagicMock(
        return_value=None
    )

    with pytest.raises(Exception):
        quiz_settings_service.get_quiz_settings(1)


def test_get_quiz_settings(quiz_settings_service: IQuizSettingsService):
    quiz = Quiz(
        id=1, creator_id=1, private_link="link", time_limit=None,
        created_at=datetime.datetime.now(), is_active=False,
    )
    quiz_settings_service.quiz_repo.get_quiz_by_id = MagicMock(
        return_value=quiz
    )

    quiz_settings = quiz_settings_service.get_quiz_settings(1)
    assert quiz_settings.is_active is False
    assert quiz_settings.private_link == quiz.private_link


def test_update_quiz_settings(quiz_settings_service: IQuizSettingsService):
    private_link = "link"
    quiz = Quiz(
        id=1, creator_id=1, private_link=private_link, time_limit=10,
        created_at=datetime.datetime.now(), is_active=False,
    )
    settings_update = QuizSettingsUpdate(
        time_limit=None, private=False,
    )

    new_settings = quiz_settings_service.update_quiz_settings(
        quiz, settings_update,
    )

    assert new_settings.private is False

    quiz.private_link = None
    settings_update.private = True

    new_settings = quiz_settings_service.update_quiz_settings(
        quiz, settings_update,
    )

    assert new_settings.private_link is not None
