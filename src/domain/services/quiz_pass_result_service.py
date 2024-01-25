from src.domain.models.answer import Answer, UserAnswer
from src.domain.models.new_types import QuestionId, QuizPassId
from src.domain.models.question import Question, QuestionType
from src.domain.models.quiz_pass import QuizPassResult
from src.domain.repos.answer import IAnswerRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.quiz import IQuizPassRepo


class QuizPassResultService:
    def __init__(
            self, quiz_pass_repo: IQuizPassRepo, question_repo: IQuestionRepo,
            answer_repo: IAnswerRepo,
    ) -> None:
        self._quiz_pass_repo = quiz_pass_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo

    def get_quiz_pass_result(self, quiz_pass_id: QuizPassId) -> QuizPassResult:
        quiz_pass_result = self._quiz_pass_repo.get_quiz_pass_result(
            quiz_pass_id,
        )
        return quiz_pass_result

    def calc_quiz_pass_result(
            self, quiz_pass_id: QuizPassId,
    ) -> QuizPassResult:
        user_answers = self._quiz_pass_repo.get_user_answers(quiz_pass_id)
        quiz_id = self._quiz_pass_repo.get_quiz_id(quiz_pass_id)
        questions = self._question_repo.get_questions_by_quiz_id(quiz_id)

        correct_answers_count = 0
        for user_answer in user_answers:
            question_id = user_answer.question_id
            question = self._get_question_by_id(questions, question_id)
            correct_answers = self._get_correct_answers(question_id)

            correct_answers_count += self._answer_is_correct(
                correct_answers, user_answer, question,
            )

        result = QuizPassResult(
            quiz_pass_id=quiz_pass_id,
            correct_answers=correct_answers_count,
            wrong_answers=len(questions) - correct_answers_count,
        )

        return result

    def _get_correct_answers(self, question_id: QuestionId) -> list[Answer]:
        answers = self._answer_repo.get_answers_by_question_id(
            question_id)
        correct_answers = filter(lambda answer: answer.is_correct, answers)

        return list(correct_answers)

    def _answer_is_correct(
            self, correct_answers: list[Answer], user_answer: UserAnswer,
            question: Question,
    ) -> bool:
        _list = [QuestionType.no_choice, QuestionType.single_choice]
        if question.question_type in _list:
            return self._single_or_no_choice_is_correct(
                correct_answers, user_answer,
            )
        elif question.question_type == QuestionType.multi_choice:
            return self._multi_choice_is_correct(correct_answers, user_answer)

    def _single_or_no_choice_is_correct(
            self, correct_answers: list[Answer], user_answer: UserAnswer
    ) -> bool:
        found = False
        for correct_answer in correct_answers:
            if correct_answer.text == user_answer.no_choice_answer:
                found += True
                break

        return found

    def _multi_choice_is_correct(
            self, correct_answers: list[Answer], user_answer: UserAnswer
    ) -> bool:
        all_found = True
        for correct_answer in correct_answers:
            found = False
            for user_choice in user_answer.choice_answer:
                if correct_answer.id == user_choice:
                    found = True
            all_found = all_found and found

        return all_found

    def _get_question_by_id(
            self, questions: list[Question], question_id: QuestionId,
    ) -> Question | None:
        for question in questions:
            if question.id == question_id:
                return question
