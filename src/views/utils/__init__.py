from typing import List
from .console import console


validate_user_input = lambda x, l: True if x in l else False
map_digit_emoji = lambda x: {
    "1": "keycap_digit_one",
    "2": "keycap_digit_two",
    "3": "keycap_digit_three",
    "4": "keycap_digit_four",
}[str(x)]

map_digit_to_alpha_emoji = lambda x: {
    "1": "regional_indicator_a",
    "2": "regional_indicator_b",
    "3": "regional_indicator_c",
    "4": "regional_indicator_d",
}[str(x)]

convert_to_alpha = lambda x: chr(x + 65)


def blocking_user_input(prompt: str, valid_resps: List, max_tries: int = 10) -> str:
    count = 0
    while True:
        if count > max_tries:
            console.print(
                "You exceed maximum tries. Exiting program right now",
                style="strong-fail",
            )
            break
        _user_input = console.input(f":backhand_index_pointing_right: {prompt}")
        if len(valid_resps) == 0:
            break

        if validate_user_input(_user_input, valid_resps):
            break

        console.print(
            f"Bummer! Thats a  wrong input! Valid responses are {valid_resps}",
            style="light-fail",
        )

        count += 1

    return _user_input
