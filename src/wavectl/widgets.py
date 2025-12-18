import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_widgets():
    console.print("[bold green]Configure Widgets[/bold green]")

    # Assuming widgets are managed via a list in settings.json or a specific widgets.json
    # For Phase 1, let's assume we can toggle some common widgets globally.

    widgets = [
        questionary.Choice("CPU Usage", checked=True),
        questionary.Choice("Memory Usage", checked=True),
        questionary.Choice("Network Speed", checked=False),
        questionary.Choice("Battery Status", checked=False),
        questionary.Choice("Weather", checked=False),
    ]

    selected_widgets = questionary.checkbox(
        "Select active widgets:",
        choices=widgets
    ).ask()

    if selected_widgets is None:
        return

    cm = ConfigManager()

    # Store as a list in settings
    cm.set_config_value("widgets", selected_widgets)

    console.print(f"[green]Successfully updated active widgets: {', '.join(selected_widgets)}[/green]")
