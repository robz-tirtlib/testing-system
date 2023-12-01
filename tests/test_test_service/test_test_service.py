import pytest

from src.domain.repos.test import ITestRepo
from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.models.test import TestSettingsIn, Test, TestSettingsUpdate
from src.domain.models.question import (
    QuestionWithCorrectAnswersCreate, QuestionType, QuestionCreate,
)
from src.domain.models.answer import AnswerCreate

from src.domain.services.test_service import TestService


regular_user_id = 1
test_creator_id = 2


@pytest.fixture
def data_for_test_creation() -> tuple:
    test_settings_in = TestSettingsIn(time_limit=0, private=False)
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
    yield test_settings_in, test_creator_id, questions


@pytest.fixture
def test(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        data_for_test_creation,
):
    test_settings_in, user_id, questions = data_for_test_creation
    _test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )

    yield _test


def test_test_creation(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        data_for_test_creation,
):
    test_settings_in, user_id, questions = data_for_test_creation
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )
    assert test is not None
    assert test.id == 1
    assert test.creator_id == test_creator_id
    assert test.private_link is None
    assert test.time_limit == 0

    # Get test for owner
    test_data_for_owner = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, user_id, False,
    )

    assert test_data_for_owner is not None
    assert len(test_data_for_owner.test.questions) == len(questions)
    assert (
        test_data_for_owner.test_settings.time_limit ==
        test_settings_in.time_limit
        )

    # Get test for user
    test_data_for_user = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, 1, False,
    )

    assert test_data_for_user is not None
    assert len(test_data_for_user.test.questions) == len(questions)


def test_adding_question(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        data_for_test_creation,
):
    test_settings_in, user_id, questions = data_for_test_creation
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )

    assert test is not None
    assert test.id == 1

    prev_questions_count = len(questions)

    test_service.add_question(
        question_repo,
        QuestionCreate(
            text="Question",
            test_id=test.id,
            question_type=QuestionType.single_choice,
        ),
    )

    test_data_for_user = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, 1, False,
    )

    assert len(test_data_for_user.test.questions) - 1 == prev_questions_count


def test_adding_answers(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        data_for_test_creation,
):
    test_settings_in, user_id, questions = data_for_test_creation
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in,
        questions, user_id,
    )

    assert test is not None
    assert test.id == 1

    prev_answers_count = len(questions[0].answers)

    test_service.add_answers(
        answer_repo,
        [AnswerCreate(
            text="Answer",
            is_correct=True,
        )],
        1,
    )

    test_data_for_owner = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, test_creator_id, False,
    )

    cur_len = len(test_data_for_owner.test.questions[0].answers)

    assert cur_len - 1 == prev_answers_count


def test_private_test_access(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
):
    test_settings_in = TestSettingsIn(time_limit=0, private=True)
    test = test_service.add_test(
        test_repo, question_repo, answer_repo, test_settings_in, [],
        test_creator_id,
    )
    with pytest.raises(Exception):
        _ = test_service.get_test(
            test_repo, question_repo, answer_repo, test.id, regular_user_id,
            False,
        )


def test_inactive_test_regular_user_access(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        test: Test,
):
    test.is_active = False

    with pytest.raises(Exception):
        _ = test_service.get_test(
            test_repo, question_repo, answer_repo, test.id, regular_user_id,
            False,
        )

    test_service.set_test_active(test.id, test_repo)

    test_data = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, regular_user_id,
        False,
    )

    assert test_data.test_settings.is_active is True


def test_update_settings_raises(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        test: Test,
):
    settings_update = TestSettingsUpdate()

    with pytest.raises(Exception):
        test_service.update_test_settings(
            test_repo, test.id, settings_update, regular_user_id,
        )


def test_update_settings(
        test_repo: ITestRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, test_service: TestService,
        test: Test,
):
    new_time_limit = 9252
    settings_update = TestSettingsUpdate(time_limit=new_time_limit)
    test_service.update_test_settings(
        test_repo, test.id, settings_update, test_creator_id,
    )

    test_data = test_service.get_test(
        test_repo, question_repo, answer_repo, test.id, test_creator_id, True,
    )

    assert test_data.test_settings.time_limit == new_time_limit
    assert test_data.test_settings.private_link == test.private_link
