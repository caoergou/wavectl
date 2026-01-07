import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_theme():
    console.print(f"[bold green]{t('Configure Theme')}[/bold green]")

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

    choices = [questionary.Choice(title=t(k), value=k) for k in themes.keys()]
    choices.append(questionary.Choice(title=t("Go Back"), value="Go Back"))

    choice = questionary.select(
        t("Select a Global Terminal Theme:"),
        choices=choices
    ).ask()

    if choice == "Go Back":
        return

    theme_value = themes[choice]

    cm = ConfigManager()

    # Set global theme in settings.json
    # Key: term:theme
    cm.set_config_value("term:theme", theme_value)

    console.print(f"[green]{t('Successfully set global theme to \'{choice}\' ({theme_value})', choice=choice, theme_value=theme_value)}[/green]")
