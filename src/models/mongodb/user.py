import datetime
from typing import List, Union, Dict
from schema import Schema, SchemaError

import pymongo
from pymongo.collection import Collection
from pymongo import results


class UserModel(Collection):
    def __init__(self, db_client: pymongo.MongoClient, db_name: str):

        super().__init__(db_client, db_name)

        self.db_client = db_client
        self.db_name = db_name

        self._schema = Schema(
            [
                {
                    "datetime": str,
                    "email": str,
                    "password": str,
                }
            ]
        )

    def put(
        self, records: Union[List, Dict]
    ) -> Union[results.InsertOneResult, results.InsertManyResult]:

        if isinstance(records, List):
            return self._put_many(records)
        else:
            return self._put_one(records)

    def _put_one(self, record: List) -> results.InsertOneResult:

        self._schema.validate([record])
        return self.insert_one(record)

    def _put_many(self, record: List) -> List[results.InsertManyResult]:

        self._schema.validate(record)
        return [self.insert_one(r) for r in record]

    def pull(self, email: str) -> dict:
        return self.find_one({"email": email})
