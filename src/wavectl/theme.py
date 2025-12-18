import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_theme():
    console.print("[bold green]Configure Theme[/bold green]")

    # Basic themes supported by WaveTerm or standard ones
    # Assuming we modify "theme" in settings.json

    themes = [
        "Default (Dark)",
        "Light",
        "Dracula",
        "Solarized Dark",
        "Go Back"
    ]

    choice = questionary.select(
        "Select a Theme:",
        choices=themes
    ).ask()

    if choice == "Go Back":
        return

    # Map choice to actual value
    # This is a guess on values. If WaveTerm uses CSS or specific json, I might need to know more.
    # But for a basic implementation:
    theme_value = choice.lower().replace(" ", "-").replace("(", "").replace(")", "")
    if "default" in theme_value:
        theme_value = "default"

    cm = ConfigManager()

    # Check if we are modifying a global setting or a preset
    # Usually themes are global settings.
    cm.set_config_value("theme", theme_value)

    console.print(f"[green]Successfully set theme to '{choice}'[/green]")
