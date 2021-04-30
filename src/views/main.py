import pymongo
from pymongo import results

from rich import markdown, rule

from src.views import WelcomeView, LoginView, RegisterView, CreateQuizView, GetQuizView
from src.views.utils.console import console
from src.views.utils import blocking_user_input


class MainView(object):
    def __init__(self, client: pymongo.MongoClient):

        self.welcome_view = WelcomeView(client, "test-user")
        self.create_quiz = CreateQuizView(client, "test-quiz")
        self.get_quiz = GetQuizView(client, "test-quiz")

    def run(self):

        console.print(markdown.HorizontalRule())

        email, auth = self.welcome_view.run()

        if auth is None:
            console.print("Quiting due to registration failure!", style="strong-fail")
        if not auth:
            console.print(
                f"No user by the id of {email}, quitting.", style="light-fail"
            )
            exit(0)

        console.print(f"\nWelcome {email}!", style="light-success", justify="center")

        while True:
            console.print(
                "\n:thinking_face: Do you want to create a quiz? Press :regional_indicator_a:!\n"
                ":thinking_face: If you want select and solve a quiz, press :regional_indicator_b:!\n"
                ":thinking_face: If you want to exit, press :regional_indicator_c: to exit"
            )

            user_res = blocking_user_input("", ["A", "B", "C"])

            if user_res == "A":
                op_res = self.create_quiz.run(email)
            elif user_res == "B":
                self.get_quiz.run()
            else:
                console.print("Exiting, Bye! :waving_hand:")
                exit(0)
