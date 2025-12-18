import typer
import questionary
from rich.console import Console

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
            console.print("[yellow]AI Settings module is under construction.[/yellow]")
        elif choice == "SSH Connections":
            console.print("[yellow]SSH Connections module is under construction.[/yellow]")
        else:
            console.print(f"[yellow]{choice} module is under construction.[/yellow]")

if __name__ == "__main__":
    app()
