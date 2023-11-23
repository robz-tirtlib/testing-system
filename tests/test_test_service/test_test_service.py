from tests.test_test_service.mocks import (
    TestRepoMock, QuestionRepoMock, AnswerRepoMock,
)

from src.domain.repos.test import ITestRepo
from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.models.test import TestSettingsIn
from src.domain.models.question import (
    QuestionWithCorrectAnswersCreate, QuestionType,
)
from src.domain.models.answer import AnswerCreate

from src.domain.services.test_service import TestService


def test_test_creation(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
):
    test_settings_in = TestSettingsIn(time_limit=0, private=False)
    user_id = 2
    questions = [
        QuestionWithCorrectAnswersCreate(
            text="What's good?",
            question_type=QuestionType.single_choice,
            answers=[
                AnswerCreate("Fine", True),
                AnswerCreate("Bad", False),
            ]
        ),
        QuestionWithCorrectAnswersCreate(
            text="If x * x = 4. Which value could x be?",
            question_type=QuestionType.single_choice,
            answers=[
                AnswerCreate("2", True),
                AnswerCreate("-2", True),
                AnswerCreate("-2", False),
            ]
        )
    ]
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )
    assert test is not None
    assert test.id == 1
    assert test.creator_id == 2
    assert test.private_link is None
    assert test.time_limit == 0

    # Get test for owner
    test_data_for_owner = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, user_id,
    )

    assert test_data_for_owner is not None
    assert len(test_data_for_owner.test.questions) == len(questions)
    assert (
        test_data_for_owner.test_settings.time_limit ==
        test_settings_in.time_limit
        )

    # Get test for user
    test_data_for_user = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, 1,
    )

    assert test_data_for_user is not None
    assert len(test_data_for_user.test.questions) == len(questions)
