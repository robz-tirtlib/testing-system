import pytest

from unittest.mock import Mock, MagicMock

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo

from src.domain.models.quiz import QuizSettingsIn, Quiz, QuizSettingsUpdate
from src.domain.models.question import (
    QuestionWithCorrectAnswersCreate, QuestionType, QuestionCreate,
)
from src.domain.models.answer import AnswerCreate

from src.domain.services.quiz_service import QuizService


regular_user_id = 1
quiz_creator_id = 2


@pytest.fixture
def data_for_quiz_creation() -> tuple:
    quiz_settings_in = QuizSettingsIn(time_limit=0, private=False)
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
    yield quiz_settings_in, quiz_creator_id, questions


@pytest.fixture
def quiz(
        quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, quiz_service: QuizService,
        data_for_quiz_creation,
):
    quiz_settings_in, user_id, questions = data_for_quiz_creation
    _quiz = quiz_service.add_quiz(
        quiz_repo, question_repo, answer_repo, quiz_settings_in,
        questions, user_id,
    )

    yield _quiz


def test_quiz_creation(
        quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, quiz_service: QuizService,
        data_for_quiz_creation,
):
    quiz_settings_in, user_id, questions = data_for_quiz_creation
    quiz = quiz_service.add_quiz(
        quiz_repo, question_repo, answer_repo, quiz_settings_in,
        questions, user_id,
    )
    assert quiz is not None
    assert quiz.id == 1
    assert quiz.creator_id == quiz_creator_id
    assert quiz.private_link is None
    assert quiz.time_limit == 0

    # Get quiz for owner
    quiz_data_for_owner = quiz_service.get_quiz(
        quiz_repo, question_repo, answer_repo, quiz.id, user_id, False,
    )

    assert quiz_data_for_owner is not None
    assert len(quiz_data_for_owner.quiz.questions) == len(questions)
    assert (
        quiz_data_for_owner.quiz_settings.time_limit ==
        quiz_settings_in.time_limit
        )

    # Get quiz for user
    quiz_data_for_user = quiz_service.get_quiz(
        quiz_repo, question_repo, answer_repo, quiz.id, 1, False,
    )

    assert quiz_data_for_user is not None
    assert len(quiz_data_for_user.quiz.questions) == len(questions)


def test_adding_question(
        quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, quiz_service: QuizService,
        data_for_quiz_creation,
):
    quiz_settings_in, user_id, questions = data_for_quiz_creation
    quiz = quiz_service.add_quiz(
        quiz_repo, question_repo, answer_repo, quiz_settings_in,
        questions, user_id,
    )

    assert quiz is not None
    assert quiz.id == 1

    prev_questions_count = len(questions)

    quiz_service.add_question(
        question_repo,
        QuestionCreate(
            text="Question",
            quiz_id=quiz.id,
            question_type=QuestionType.single_choice,
        ),
    )

    quiz_data_for_user = quiz_service.get_quiz(
        quiz_repo, question_repo, answer_repo, quiz.id, 1, False,
    )

    assert len(quiz_data_for_user.quiz.questions) - 1 == prev_questions_count


def test_adding_answers(
        quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, quiz_service: QuizService,
        data_for_quiz_creation,
):
    quiz_settings_in, user_id, questions = data_for_quiz_creation
    quiz = quiz_service.add_quiz(
        quiz_repo, question_repo, answer_repo, quiz_settings_in,
        questions, user_id,
    )

    assert quiz is not None
    assert quiz.id == 1

    prev_answers_count = len(questions[0].answers)

    quiz_service.add_answers(
        answer_repo,
        [AnswerCreate(
            text="Answer",
            is_correct=True,
        )],
        1,
    )

    quiz_data_for_owner = quiz_service.get_quiz(
        quiz_repo, question_repo, answer_repo, quiz.id, quiz_creator_id, False,
    )

    cur_len = len(quiz_data_for_owner.quiz.questions[0].answers)

    assert cur_len - 1 == prev_answers_count


def test_get_non_existent_quiz(quiz_service: QuizService):
    quiz_repo = Mock()
    quiz_repo.get_quiz_by_id = MagicMock(return_value=None)

    with pytest.raises(Exception):
        quiz_service.get_quiz(
            quiz_repo, Mock(), Mock(), Mock(), Mock(), Mock(),
        )


def test_private_quiz_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.private_link = "link"
    quiz_repo = Mock()
    quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)

    with pytest.raises(Exception):
        _ = quiz_service.get_quiz(
            quiz_repo, Mock(), Mock(), Mock(), Mock(), False,
        )


def test_inactive_quiz_regular_user_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.creator_id = quiz_creator_id
    quiz_repo = Mock()
    quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)
    quiz._get_quiz_for_user = MagicMock()

    with pytest.raises(Exception):
        _ = quiz_service.get_quiz(
            quiz_repo, Mock(), Mock(), Mock(), regular_user_id,
            False,
        )


def test_inactive_quiz_owner_access(quiz_service: QuizService):
    quiz = Mock()
    quiz.creator_id = quiz_creator_id
    quiz_repo = Mock()
    quiz_repo.get_quiz_by_id = MagicMock(return_value=quiz)
    quiz_service._get_quiz_for_owner = MagicMock()

    _ = quiz_service.get_quiz(
        quiz_repo, Mock(), Mock(), Mock(), quiz_creator_id,
        True,
    )


def test_update_settings_raises(
        quiz_repo: IQuizRepo, quiz_service: QuizService, quiz: Quiz,
):
    settings_update = QuizSettingsUpdate()

    with pytest.raises(Exception):
        quiz_service.update_quiz_settings(
            quiz_repo, quiz.id, settings_update, regular_user_id,
        )


def test_update_settings(
        quiz_repo: IQuizRepo, question_repo: IQuestionRepo,
        answer_repo: IAnswerRepo, quiz_service: QuizService,
        quiz: Quiz,
):
    new_time_limit = 9252
    settings_update = QuizSettingsUpdate(time_limit=new_time_limit)
    quiz_service.update_quiz_settings(
        quiz_repo, quiz.id, settings_update, quiz_creator_id,
    )

    quiz_data = quiz_service.get_quiz(
        quiz_repo, question_repo, answer_repo, quiz.id, quiz_creator_id, True,
    )

    assert quiz_data.quiz_settings.time_limit == new_time_limit
    assert quiz_data.quiz_settings.private_link == quiz.private_link
