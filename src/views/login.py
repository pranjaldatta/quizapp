from typing import List, Tuple
import pymongo

from rich import bar, markdown
from src.controllers.auth_controller import AuthController
from src.views.utils.console import console
from src.views.utils import blocking_user_input


class LoginView(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):
        self.ac = AuthController(client, db_name)

    def run(self) -> Tuple[str, bool]:

        console.print(markdown.HorizontalRule())

        console.print("Login", justify="center", style="blue")

        email = blocking_user_input("email: ", [])
        candidate_pass = blocking_user_input("password: ", [])

        auth_status = self.ac.verify_user(email, candidate_pass)

        console.print(markdown.HorizontalRule())

        return email, auth_status
