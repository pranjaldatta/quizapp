import pymongo
from pymongo import results

from rich import markdown
import datetime

from src.controllers.quiz_controller import QuizController
from src.views.utils import blocking_user_input
from src.views.utils.console import console


class CreateQuizView(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):
        self.qc = QuizController(client, db_name)

    def run(self, email: str) -> bool:

        console.print(markdown.HorizontalRule())
        console.print("Create a Quiz!", justify="center", style="blue")

        console.print(
            "\n:nerd_face: Lets help you make a quiz. Just keep answering the prompt and in no time, "
            "your own quiz would be up and running!"
        )

        console.print(
            "So Here we go! :chequered_flag: :backhand_index_pointing_down:",
            style="light-success",
        )

        console.print(
            "\n:thinking_face: What should be the name of the quiz?",
            style="blue",
        )
        quiz_name = blocking_user_input("", [])

        author_name = email
        timestamp = str(datetime.datetime.now())

        console.print(
            "\n:thinking_face: How many questions are there in this quiz? (Note: let's just cap it 5 please)?",
            style="blue",
        )
        num_questions = int(blocking_user_input("", ["1", "2", "3", "4", "5"]))

        question_list = []

        for i in range(1, num_questions + 1):
            console.print(
                f"\n:thinking_face: What is question number #{i}?",
                style="blue",
            )
            _ques = blocking_user_input("", [])
            _options = []
            for j in range(1, 5):
                _opt = blocking_user_input(f"Option #{j}? ", [])
                _options.append(_opt)

            console.print(
                f"\n:thinking_face: What is the correct choice? [Note: It has to be out of 1, 2, 3, 4]?",
                style="blue",
            )
            _ans = int(blocking_user_input("", ["1", "2", "3", "4"])) - 1

            question_list.append(
                {"qno": i, "ques": _ques, "options": _options, "ans": _ans}
            )

        quiz_record = {
            "quiz_name": quiz_name,
            "author": email,
            "datetime": timestamp,
            "num_questions": num_questions,
            "questions": question_list,
        }

        response = self.qc.create_quiz(quiz_record)

        console.print(markdown.HorizontalRule())
        if isinstance(response, pymongo.results.InsertOneResult):
            return True

        return False
