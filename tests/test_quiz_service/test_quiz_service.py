import pytest

from unittest.mock import Mock, MagicMock

from src.domain.services.quiz_service import QuizService


regular_user_id = 1
quiz_creator_id = 2


def test_get_non_existent_quiz(quiz_service: QuizService):
    quiz_service.quiz_repo = MagicMock(return_value=None)

    with pytest.raises(Exception):
        quiz_service.get_quiz(
            Mock(), Mock(), Mock(), Mock(), Mock(),
        )


def test_private_quiz_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.private_link = "link"
    quiz_service.quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)

    with pytest.raises(Exception):
        _ = quiz_service.get_quiz(
            Mock(), Mock(), Mock(), Mock(), False,
        )


def test_inactive_quiz_regular_user_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.creator_id = quiz_creator_id
    quiz_service.quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)
    quiz_service._get_quiz_for_user = MagicMock()

    with pytest.raises(Exception):
        _ = quiz_service.get_quiz(
            Mock(), Mock(), Mock(), regular_user_id,
            False,
        )


def test_inactive_quiz_owner_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.creator_id = quiz_creator_id
    quiz_service.quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)
    quiz_service._get_quiz_for_owner = MagicMock()

    _ = quiz_service.get_quiz(
        Mock(), Mock(), Mock(), quiz_creator_id,
        True,
    )


def test_not_owner_updating_settings(quiz_service: QuizService):
    quiz = Mock()
    quiz.creator_id = quiz_creator_id
    quiz_service.quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)

    with pytest.raises(Exception):
        quiz_service.update_quiz_settings(
            Mock(), Mock(), regular_user_id,
        )
