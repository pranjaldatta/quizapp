import pymongo
from pymongo import results
import random
import hashlib
import datetime

from src.models.mongodb.user import UserModel


class AuthController(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):

        self.data_model = UserModel(client, db_name)
        self.algo = "sha1"

    def _set_pass_hash(self, raw_password: str) -> str:

        raw_password = raw_password.encode("utf-8")
        salt = self._get_salt(raw_password)
        hsh = getattr(hashlib, self.algo)(raw_password + salt).hexdigest()
        return hsh

    def _get_salt(self, raw_password: str) -> str:
        return raw_password[:5] if len(raw_password) > 4 else raw_password

    def _compare_with_hash(self, candidate: str, hashed_pass: str) -> bool:
        return self._set_pass_hash(candidate) == hashed_pass

    def onboard_user(self, email: str, raw_password: str) -> results.InsertOneResult:
        return self.data_model.put(
            {
                "datetime": str(datetime.datetime.now()),
                "email": email,
                "password": self._set_pass_hash(raw_password),
            }
        )

    def verify_user(self, email: str, candidate_pass: str) -> bool:
        _record = self.data_model.pull(email)
        if _record is None:
            return False
        return self._compare_with_hash(candidate_pass, _record["password"])
