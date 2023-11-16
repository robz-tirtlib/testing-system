from dataclasses import dataclass
from typing import NewType
from enum import Enum

from .test import TestId


QuestionId = NewType("QuestionId", int)


class QuestionType(Enum):
    no_choice = 0
    single_choice = 1
    multi_choice = 2


@dataclass
class Question:
    id: QuestionId
    test_id: TestId
    text: str
    question_type: QuestionType


@dataclass
class QuestionCreate:
    test_id: TestId
    text: str
    question_type: QuestionType
