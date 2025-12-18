import typer
import questionary
from rich.console import Console
from .ai import configure_ai_settings
from .ssh import configure_ssh_connections
from .theme import configure_theme
from .widgets import configure_widgets

app = typer.Typer()
console = Console()

@app.command()
def main():
    """
    WaveCtl: Interactive WaveTerm Configuration Manager.
    """
    console.print("[bold blue]Welcome to WaveCtl![/bold blue]")
    console.print("Manage your WaveTerm configuration with ease.\n")

    while True:
        choice = questionary.select(
            "What would you like to configure?",
            choices=[
                "AI Settings",
                "SSH Connections",
                "Themes",
                "Widgets",
                questionary.Separator(),
                "Exit"
            ]
        ).ask()

        if choice == "Exit":
            console.print("Goodbye!")
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
            console.print(f"[yellow]{choice} module is under construction.[/yellow]")

if __name__ == "__main__":
    app()
