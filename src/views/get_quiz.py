import pymongo
from pymongo import results

from rich import markdown, rule, spinner, segment
import datetime

from src.controllers.quiz_controller import QuizController
from src.views.utils import blocking_user_input
from src.views.utils.console import console
from src.views.utils import map_digit_emoji, map_digit_to_alpha_emoji, convert_to_alpha


class GetQuizView(object):
    def __init__(self, client: pymongo.MongoClient, db_name: str):
        self.qc = QuizController(client, db_name)

    def run(self) -> None:

        console.print(markdown.HorizontalRule())
        console.print("Quiz View", justify="center", style="blue")
        console.print("Here are the available quizzes!", justify="center", style="blue")

        avail_quizzes = self.qc.list_quiz()

        for i, item in enumerate(avail_quizzes):
            console.print(
                f":backhand_index_pointing_right: {i+1}. [under-success]{item['quiz_name']}[/under-success] by [yellow]{item['author']}[/yellow]. [NoQ -> {item['num_questions']}]"
            )

        console.print("\n:nerd_face: So, which quiz you want to choose?")
        user_choice = int(
            blocking_user_input("", [str(i + 1) for i in range(len(avail_quizzes))])
        )

        console.print(rule.Rule("The quiz begins :backhand_index_pointing_down:"))

        quiz = avail_quizzes[user_choice - 1]
        questions = quiz["questions"]
        console.print(
            f"\n[yellow]:beaming_face_with_smiling_eyes: Quiz Name:[/yellow] {quiz['quiz_name']}"
        )
        console.print(
            f"[yellow]:beaming_face_with_smiling_eyes: Quiz Author:[/yellow] {quiz['author']}"
        )
        console.print(
            f"[yellow]:beaming_face_with_smiling_eyes: Number of Questions:[/yellow] {quiz['num_questions']}"
        )
        console.print(
            f"[yellow]:beaming_face_with_smiling_eyes: Time added:[/yellow] {quiz['datetime']}"
        )

        candidate_answers = []
        for i, qi in enumerate(questions):
            console.print(f"\n:thinking_face: Q{i+1}) {qi['ques']}", style="yellow")
            console.print("Options are given :backhand_index_pointing_down:")

            for j in range(1, 5):
                console.print(f":{map_digit_to_alpha_emoji(j)}:   {qi['options'][j-1]}")
            _choice = ord(blocking_user_input("", ["A", "B", "C", "D"])) - 65
            candidate_answers.append(_choice)

        report, score = self.qc.score_explicit(candidate_answers, questions)

        console.print("\nReport :backhand_index_pointing_down:", style="blue")
        console.print(
            f"\n[strong-success]Final Score:[/strong-success] {score} / {len(report)}"
        )

        count = 1
        console.print(
            "\n[under-success]Detailed report below[/under-success] :backhand_index_pointing_down:\n"
        )
        for qi, ai, ri in zip(questions, candidate_answers, report):
            console.print(
                f":{'white_heavy_check_mark' if ri else 'cross_mark'}:", end=" "
            )
            console.print(f"Q{count}) {qi['ques']}", style="underline", end="")
            console.print(" | ", end="")

            console.print(
                f"Your Answer: {convert_to_alpha(ai)}, Correct Answer: {convert_to_alpha(qi['ans'])}",
                style="light-success" if ri else "light-fail",
            )

        console.print(markdown.HorizontalRule())
