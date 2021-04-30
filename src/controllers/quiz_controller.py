import pymongo
from pymongo import results
from typing import Dict, List, Tuple

from src.models.mongodb import QuizModel


class QuizController(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):

        self.data_model = QuizModel(client, db_name)
        self.current_quiz = None

    def create_quiz(self, records: Dict) -> results.InsertOneResult:
        return self.data_model.create_quiz(records)

    def list_quiz(self) -> List[Dict]:
        return list(self.data_model.list_quiz())

    def pull_quiz(self, quiz_name: str) -> Dict:
        self.current_quiz = self.data_model.pull_quiz(quiz_name)
        return self.current_quiz

    def score(self, answers: List[int]) -> Tuple[List, int]:

        _keys = self.current_quiz["questions"]
        assert len(_keys) == len(answers)

        report = [k["ans"] == a for k, a in zip(_keys, answers)]

        return report, sum(report)

    def score_explicit(
        self, candidate_answers: List[int], questions: List[dict]
    ) -> Tuple[List, int]:

        assert len(candidate_answers) == len(questions)
        print(questions, candidate_answers)
        report = [qi["ans"] == ai for qi, ai in zip(questions, candidate_answers)]

        return report, sum(report)
