from rich.console import Console
from rich.theme import Theme

console_style_params = Theme(
    {
        "light-success": "green",
        "strong-success": "bold green",
        "under-success": "underline green",
        "under-strong-success": "underline bold green",
        "light-fail": "red",
        "strong-fail": "bold red",
        "under-strong-fail": "underline bold red",
        "blue": "blue",
        "yellow": "yellow",
        "underline": "underline",
    }
)

console = Console(theme=console_style_params)
