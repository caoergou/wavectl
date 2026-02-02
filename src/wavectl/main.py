import typer
import questionary
from rich.console import Console
from .ai import configure_ai_settings
from .ssh import configure_ssh_connections
from .theme import configure_theme
from .widgets import configure_widgets
from .settings import configure_general_settings
from .i18n import t, set_language
from .config_manager import ConfigManager

app = typer.Typer()
console = Console()

@app.command()
def main():
    """
    WaveCtl: Interactive WaveTerm Configuration Manager.
    """
    # Startup language check
    cm = ConfigManager()
    config = cm.load_wavectl_config()
    if not config.get("lang"):
        lang_choice = questionary.select(
            "Select Language / 选择语言:",
            choices=[
                questionary.Choice(title="English", value="en_US"),
                questionary.Choice(title="中文", value="zh_CN")
            ]
        ).ask()
        if lang_choice:
            set_language(lang_choice)

    console.print(f"[bold blue]{t('Welcome to WaveCtl!')}[/bold blue]")
    console.print(t("Manage your WaveTerm configuration with ease.\n"))

    while True:
        choice = questionary.select(
            t("What would you like to configure?"),
            choices=[
                questionary.Choice(title=t("AI Settings"), value="AI Settings"),
                questionary.Choice(title=t("SSH Connections"), value="SSH Connections"),
                questionary.Choice(title=t("Themes"), value="Themes"),
                questionary.Choice(title=t("Widgets"), value="Widgets"),
                questionary.Choice(title=t("General Settings"), value="General Settings"),
                questionary.Separator(),
                questionary.Choice(title=t("Exit"), value="Exit")
            ]
        ).ask()

        if choice == "Exit":
            console.print(t("Goodbye!"))
            break
        elif choice == "AI Settings":
            configure_ai_settings()
        elif choice == "SSH Connections":
            configure_ssh_connections()
        elif choice == "Themes":
            configure_theme()
        elif choice == "Widgets":
            configure_widgets()
        elif choice == "General Settings":
            configure_general_settings()
        else:
            console.print(f"[yellow]{t('{choice} module is under construction.', choice=choice)}[/yellow]")

if __name__ == "__main__":
    app()
