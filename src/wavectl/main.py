import typer
import questionary
from rich.console import Console
from .ai import configure_ai_settings

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
                "Themes (Coming Soon)",
                "Widgets (Coming Soon)",
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
            console.print("[yellow]SSH Connections module is under construction.[/yellow]")
        else:
            console.print(f"[yellow]{choice} module is under construction.[/yellow]")

if __name__ == "__main__":
    app()
