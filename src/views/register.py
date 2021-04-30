from typing import List
import pymongo

from rich import bar, markdown
from src.controllers.auth_controller import AuthController
from src.views.utils.console import console
from src.views.utils import blocking_user_input


class RegisterView(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):
        self.ac = AuthController(client, db_name)

    def run(self) -> pymongo.results.InsertOneResult:

        console.print(markdown.HorizontalRule())

        console.print("Register a new user!", justify="center", style="blue")

        email = blocking_user_input(
            "Enter your email (this acts as your username): ", []
        )
        password = blocking_user_input(
            "Enter a password (we store it securely with hashing!): ", []
        )

        user_obj = self.ac.onboard_user(email, password)

        if isinstance(user_obj, pymongo.results.InsertOneResult):
            console.print(
                "Congratulations! Registered as a new user!", style="light-success"
            )
        console.print(markdown.HorizontalRule())

        return email, user_obj
