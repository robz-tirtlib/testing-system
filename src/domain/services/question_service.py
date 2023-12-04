from abc import ABC, abstractmethod
from src.domain.models.answer import PossibleAnswer

from src.domain.models.new_types import QuestionId, QuizId
from src.domain.models.question import (
    Question, QuestionCreate, QuestionWithAnswersCreate,
    QuestionWithPossibleAnswers,
)
from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo


class IQuestionService(ABC):
    @abstractmethod
    def get_quiz_questions(self, quiz_id: QuizId) -> list[Question]:
        raise NotImplementedError

    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        raise NotImplementedError

    @abstractmethod
    def get_quiz_questions_with_possible_answers(
        self, quiz_id: QuizId,
    ) -> list[QuestionWithPossibleAnswers]:
        raise NotImplementedError

    @abstractmethod
    def add_questions_with_answers(
        self, questions_with_answers: list[QuestionWithAnswersCreate],
        quiz_id: QuizId,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_question_with_answers(
        self, question_with_answers: QuestionWithAnswersCreate,
        quiz_id: QuizId,
    ) -> None:
        raise NotImplementedError


class QuestionService(IQuestionService):

    def __init__(
            self, question_repo: IQuestionRepo, answer_repo: IAnswerRepo,
    ) -> None:
        self.question_repo = question_repo
        self.answer_repo = answer_repo

    def get_quiz_questions(self, quiz_id: QuizId) -> list[Question]:
        quiz_questions = self.question_repo.get_questions_by_quiz_id(quiz_id)
        return quiz_questions

    def get_question_by_id(self, question_id: QuestionId) -> Question | None:
        question = self.question_repo.get_question_by_id(question_id)
        return question

    def get_quiz_questions_with_possible_answers(
            self, quiz_id: QuizId,
    ) -> list[QuestionWithPossibleAnswers]:
        questions = self.question_repo.get_questions_by_quiz_id(quiz_id)
        questions_with_possible_answers = []

        for question in questions:
            possible_answers = self._get_question_possbible_answers(question)
            question_with_possible_answers = QuestionWithPossibleAnswers(
                id=question.id,
                quiz_id=question.quiz_id,
                text=question.text,
                question_type=question.question_type,
                possible_answers=possible_answers,
            )
            questions_with_possible_answers.append(
                question_with_possible_answers,
            )

    def _get_question_possbible_answers(
            self, question: Question,
    ) -> list[PossibleAnswer]:
        answers = self.answer_repo.get_answers_by_question_id(question.id)
        possible_answers = []

        for answer in answers:
            possible_answer = PossibleAnswer(
                id=answer.id,
                question_id=answer.question_id,
                text=answer.text,
            )
            possible_answers.append(possible_answer)

        return possible_answers

    def add_questions_with_answers(
            self, questions_with_answers: list[QuestionWithAnswersCreate],
            quiz_id: QuizId,
    ) -> None:
        for question_with_answers in questions_with_answers:
            self.add_question_with_answers(
                question_with_answers, quiz_id,
            )

    def add_question_with_answers(
            self, question_with_answers: QuestionWithAnswersCreate,
            quiz_id: QuizId,
    ) -> None:
        question_create = QuestionCreate(
            quiz_id=quiz_id,
            text=question_with_answers.text,
            question_type=question_with_answers.question_type,
        )
        question = self.question_repo.create_question(
            question_create, quiz_id,
        )
        self.answer_repo.create_answers(
            question_with_answers.answers, question.id,
        )
