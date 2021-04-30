import datetime
from typing import List, Union, Dict
from schema import Schema, SchemaError, And

import pymongo
from pymongo.collection import Collection
from pymongo import results


class QuizModel(Collection):
    def __init__(self, db_client: pymongo.MongoClient, db_name: str):

        super().__init__(db_client, db_name)

        self.db_client = db_client
        self.db_name = db_name

        self._schema = Schema(
            {
                "quiz_name": str,
                "author": str,
                "datetime": str,
                "num_questions": int,
                "questions": [
                    {
                        "qno": int,
                        "ques": str,
                        "options": And([str], lambda n: len(n) < 5),
                        "ans": int,
                    }
                ],
            }
        )

    def create_quiz(self, records: Dict) -> results.InsertOneResult:

        self._schema.validate(records)
        assert records["num_questions"] == len(records["questions"])

        return self.insert_one(records)

    def pull_quiz(self, quiz_name: str) -> None:

        return self.find_one({"quiz_name": quiz_name})

    def list_quiz(self) -> List[Dict]:
        return self.find({})
