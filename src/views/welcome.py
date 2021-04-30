import pymongo
from typing import Union, List, Tuple
from src.views.utils.console import console
from src.controllers.auth_controller import AuthController
from src.views.utils import validate_user_input, blocking_user_input
from src.views.login import LoginView
from src.views.register import RegisterView


class WelcomeView(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str, max_tries: int = 5):
        self.max_tries = max_tries
        self.ac = AuthController(client, db_name)

        self.login_webview = LoginView(client, db_name)
        self.register_webview = RegisterView(client, db_name)

    def run(self) -> Union[Tuple[str, bool], bool]:
        console.print(
            "Hello World! Welcome to our Quiz App!", justify="center", style="blue"
        )
        console.print(
            "This is a (very) simple terminal-based quiz app."
            "While simply designed, this app is connected to a live database!",
            justify="center",
            style="blue",
        )
        console.print(
            "\n[:white_check_mark:] Take quizes and look at a detailed scorecard!\n"
            "[:white_check_mark:] Create your own quizes!"
        )

        console.print(
            "\nAre you a visiting User? Press :regional_indicator_a:  to log in!\n"
            "If you are new here, press :regional_indicator_b:  to sign-up!\n"
            "If you want to exit, press :regional_indicator_c: to exit"
        )

        user_res = blocking_user_input("", ["A", "B", "C"])

        if user_res == "A":
            return self.login_webview.run()
        elif user_res == "B":
            email, res = self.register_webview.run()

            if isinstance(res, pymongo.results.InsertOneResult):
                return email, True
            else:
                console.print("Snap! Could not register user :sad_but_relieved_face:")
        else:
            console.print("Exiting, Bye! :waving_hand:")
            exit(0)
        return None, None
