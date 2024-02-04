from src.domain.dto.answer import AnswerCreate
from src.domain.dto.question import QuestionCreate

from src.domain.models.new_types import QuizId
from src.domain.models.question import Question, QuestionType

from src.domain.exceptions.question import (
    QuestionTypeError, TooFewAnswersError, TooManyAnswersError,
)


class QuestionService:
    def create_question(
            self, quiz_id: QuizId, text: str, question_type: str,
    ) -> QuestionCreate:
        if not QuestionType.has(question_type):
            raise QuestionTypeError(question_type)

        return QuestionCreate(
            quiz_id=quiz_id,
            text=text,
            question_type=question_type,
            )

    def validate_answers(
            self, question: Question, answers: list[AnswerCreate],
    ) -> list[AnswerCreate]:
        correct_answers_count = sum([answer.is_correct for answer in answers])

        one_answer_types = [QuestionType.no_choice, QuestionType.single_choice]
        if (question.question_type in one_answer_types
                and correct_answers_count > 1):
            raise TooManyAnswersError(question.id)

        if (question.question_type in QuestionType.multi_choice
                and correct_answers_count < 2):
            raise TooFewAnswersError(question.id)

        if correct_answers_count == 0:
            raise TooFewAnswersError(question.id)
