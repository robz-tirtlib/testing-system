import datetime

from src.domain.models.quiz import Quiz
from src.domain.models.user import User
from src.domain.services.permission_service import PermissionService


def test_user_can_update_quiz_settings():
    permission_service = PermissionService()
    user = User(id=1, username="", email="")
    quiz = Quiz(
        id=1, creator_id=1, private_link="", time_limit="",
        created_at=datetime.datetime.now(), is_active=True,
    )

    assert permission_service.user_can_update_quiz_settings(
        user, quiz,
    ) is True

    user.id = 2

    assert permission_service.user_can_update_quiz_settings(
        user, quiz,
    ) is False
