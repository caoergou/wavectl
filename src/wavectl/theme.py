import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_theme():
    console.print("[bold green]Configure Theme[/bold green]")

    # Themes from termthemes.json (default ones)
    themes = {
        "Default Dark": "default-dark",
        "One Dark Pro": "onedarkpro",
        "Dracula": "dracula",
        "Monokai": "monokai",
        "Campbell": "campbell",
        "Warm Yellow": "warmyellow",
        "Rose Pine": "rosepine"
    }

    choices = list(themes.keys()) + ["Go Back"]

    choice = questionary.select(
        "Select a Global Terminal Theme:",
        choices=choices
    ).ask()

    if choice == "Go Back":
        return

    theme_value = themes[choice]

    cm = ConfigManager()

    # Set global theme in settings.json
    # Key: term:theme
    cm.set_config_value("term:theme", theme_value)

    console.print(f"[green]Successfully set global theme to '{choice}' ({theme_value})[/green]")
