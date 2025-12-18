import typer
import questionary
from rich.console import Console
from .ai import configure_ai_settings
from .ssh import configure_ssh_connections
from .theme import configure_theme
from .widgets import configure_widgets
from .i18n import t

app = typer.Typer()
console = Console()

@app.command()
def main():
    """
    WaveCtl: Interactive WaveTerm Configuration Manager.
    """
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
        else:
            console.print(f"[yellow]{t('{choice} module is under construction.', choice=choice)}[/yellow]")

if __name__ == "__main__":
    app()
