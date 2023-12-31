import datetime

from src.domain.models.new_types import UserId, QuizPassId
from src.domain.models.quiz import Quiz
from src.domain.models.quiz_pass import (
    QuizPassCreate, QuizPass, QuizPassOwnerDetails,
)
from src.domain.models.question import QuestionWithAllAnswers, Question
from src.domain.models.answer import UserAnswer, Answer

from src.domain.repos.quiz import IQuizRepo, IQuizPassRepo
from src.domain.repos.question import IQuestionRepo
from src.domain.repos.answer import IAnswerRepo


class QuizPassService:
    def start_quiz_pass(
            self, quiz_pass: QuizPassCreate, quiz_pass_repo: IQuizPassRepo,
    ) -> QuizPass:
        return quiz_pass_repo.create_quiz_pass(quiz_pass)

    def end_quiz_pass(
            self, quiz_pass_repo: IQuizPassRepo, quiz_pass_id: QuizPassId,
            user_id: UserId,
    ) -> None:
        quiz_pass = quiz_pass_repo.get_quiz_pass_by_id(quiz_pass_id)

        if quiz_pass is None:
            # TODO: custom exception
            raise Exception("There is no such quiz pass going on.")

        if quiz_pass.user_id != user_id:
            # TODO: custom exception
            raise Exception("No access.")

        quiz_pass_repo.finish_quiz_pass(quiz_pass_id)

    def get_details(
            self, quiz_pass_id: QuizPassId, user_id: UserId,
            quiz_repo: IQuizRepo, quiz_pass_repo: IQuizPassRepo,
            answer_repo: IAnswerRepo, question_repo: IQuestionRepo,
    ) -> None:
        quiz_pass = quiz_pass_repo.get_quiz_pass_by_id(quiz_pass_id)
        quiz = quiz_repo.get_quiz_by_id(quiz_pass.quiz_id)

        if quiz_pass is None or quiz is None:
            return  # TODO: raise custom exception

        if user_id == quiz.creator_id:
            return self._details_for_owner(
                quiz, user_id, quiz_pass, question_repo, answer_repo,
            )

        if user_id == quiz_pass.user_id:
            return self._details_for_user()

        # TODO: custom access Exception
        raise Exception("You do not have access to these details.")

    def _details_for_owner(
            self, quiz: Quiz, user_id: UserId, quiz_pass: QuizPass,
            question_repo: IQuestionRepo, answer_repo: IAnswerRepo,
    ) -> QuizPassOwnerDetails:
        questions_with_user_answers = self._get_questions_with_user_answers(
            question_repo, quiz, answer_repo, quiz_pass, user_id,
        )

        # TODO: Allow not limited quizs
        is_finished = self._is_quiz_pass_finished(quiz, quiz_pass)
        quiz_pass_owner_details = QuizPassOwnerDetails(
            quiz_id=quiz.id,
            quiz_pass_id=quiz_pass.id,
            user_id=user_id,
            started_at=quiz_pass.started_at,
            is_finished=is_finished,
            questions=questions_with_user_answers,
        )

        return quiz_pass_owner_details

    def _is_quiz_pass_finished(
            self, quiz: Quiz, quiz_pass: QuizPass,
    ) -> bool:
        time_delta = datetime.timedelta(seconds=quiz.time_limit)
        quiz_ending = quiz_pass.started_at + time_delta
        is_finished = True if quiz_ending <= datetime.datetime.now() else False

        return is_finished | quiz_pass.is_finished

    def _get_questions_with_user_answers(
            self, question_repo: IQuestionRepo, quiz: Quiz,
            answer_repo: IAnswerRepo, quiz_pass: QuizPass,
            user_id: UserId,
    ) -> list[QuestionWithAllAnswers]:
        questions_with_user_answers: list[QuestionWithAllAnswers] = []

        for question in question_repo.get_questions_by_quiz_id(quiz.id):
            question_with_user_answers = self._get_question_with_user_answers(
                answer_repo, question, quiz_pass, user_id, quiz,
            )
            questions_with_user_answers.append(question_with_user_answers)

        return questions_with_user_answers

    def _get_question_with_user_answers(
            self, answer_repo: IAnswerRepo, question: Question,
            quiz_pass: QuizPass, user_id: UserId, quiz: Quiz,
    ) -> QuestionWithAllAnswers:
        answers = answer_repo.get_answers_by_question_id(question.id)
        user_answers = answer_repo.get_user_answers(
            quiz_pass_id=quiz_pass.id,
            question_id=question.id,
            user_id=user_id,
        )

        is_correct = self._is_user_correct(answers, user_answers)

        question_with_user_answers = QuestionWithAllAnswers(
            id=question.id,
            quiz_id=quiz.id,
            text=question.text,
            question_type=question.question_type,
            answers=answers,
            user_answers=user_answers,
            is_correct=is_correct,
        )

        return question_with_user_answers

    def _is_user_correct(
            self, answers: list[Answer], user_answers: list[UserAnswer]
    ) -> bool:
        # TODO: Check for no_choice questions

        is_correct = True
        for answer in answers:
            if answer.is_correct is False:
                continue

            found = False
            for user_answer in user_answers:
                if user_answer.answer_id == answer.id:
                    found = True
            if found is False:
                is_correct = False

        return is_correct

    def _details_for_user(self):
        return
