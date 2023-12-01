import datetime

from src.domain.models.new_types import (
    UserId, QuizId, QuestionId, AnswerId, QuizPassId,
)

from src.domain.models.quiz import Quiz, QuizSettingsFull
from src.domain.models.question import Question, QuestionCreate
from src.domain.models.answer import Answer, AnswerCreate, UserAnswer

from src.domain.repos.quiz import IQuizRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo


class QuizRepoMock(IQuizRepo):
    def __init__(self) -> None:
        self.quizs: dict[int, Quiz] = {}
        self._quiz_id = 1

    def get_quiz_by_id(self, quiz_id: QuizId) -> Quiz | None:
        return self.quizs.get(quiz_id, None)

    def create_quiz(
            self, quiz_settings: QuizSettingsFull,
            user_id: UserId
    ) -> Quiz:
        quiz = Quiz(
            id=self._quiz_id,
            creator_id=user_id,
            private_link=quiz_settings.private_link,
            time_limit=quiz_settings.time_limit,
            created_at=datetime.datetime.now(),
        )
        self.quizs[1] = quiz

        self._quiz_id += 1
        return quiz

    def update_is_active(
            self, quiz_id: QuizId, change_to_active: bool
    ) -> None:
        quiz = self.quizs.get(quiz_id, None)

        if quiz is None:
            return False

        if change_to_active:
            quiz.is_active = True
        else:
            quiz.is_active = False
        return True

    def update_quiz_settings(
            self, quiz_id: QuizId, quiz_settings: QuizSettingsFull
    ) -> None:
        quiz = self.quizs.get(quiz_id)
        quiz.time_limit = quiz_settings.time_limit
        quiz.private_link = quiz_settings.private_link
        quiz.is_active = quiz_settings.is_active


class QuestionRepoMock(IQuestionRepo):
    def __init__(self) -> None:
        self.questions: dict[int, Question] = {}
        self._question_id = 1

    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        return self.questions.get(question_id, None)

    def get_questions_by_quiz_id(
        self, quiz_id: QuizId,
    ) -> list[Question]:
        questions = []

        for _, question in self.questions.items():
            if question.quiz_id == quiz_id:
                questions.append(question)

        return questions

    def create_questions(
        self, questions: list[QuestionCreate],
    ) -> list[Question]:
        created_questions = []

        for question in questions:
            created_question = Question(
                id=self._question_id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
            )
            self.questions[self._question_id] = created_question
            created_questions.append(created_question)

            self._question_id += 1
        return created_questions

    def create_question(self, question: QuestionCreate) -> Question:
        created_question = Question(
                id=self._question_id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
            )
        self.questions[self._question_id] = created_question
        self._question_id += 1

        return created_question


class AnswerRepoMock(IAnswerRepo):
    def __init__(self) -> None:
        self.answers: dict[int, Answer] = {}
        self._answer_id = 1

    def get_answer_by_id(self, answer_id: AnswerId) -> Answer | None:
        return self.answers.get(answer_id, None)

    def get_answers_by_question_id(
        self, question_id: QuestionId
    ) -> list[Answer]:
        answers = []

        for _, answer in self.answers.items():
            if answer.question_id == question_id:
                answers.append(answer)

        return answers

    def get_user_answers(
        self, quiz_pass_id: QuizPassId, question_id: QuestionId,
        user_id: UserId,
    ) -> list[UserAnswer]:
        raise NotImplementedError

    def create_answers(
        self, answers: list[AnswerCreate], question_id: QuestionId,
    ) -> list[Answer]:
        created_answers = []

        for answer in answers:
            created_answer = Answer(
                id=self._answer_id,
                question_id=question_id,
                text=answer.text,
                is_correct=answer.is_correct,
            )
            self.answers[self._answer_id] = created_answer
            created_answers.append(created_answer)
            self._answer_id += 1

        return created_answers

    def create_user_answers(
        self, quiz_pass_id: QuizPassId, question_id: QuestionId,
        answer_id: AnswerId, user_id: UserId,
    ) -> UserAnswer:
        raise NotImplementedError
