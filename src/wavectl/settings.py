import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_general_settings():
    console.print(f"[bold green]{t('Configure General Settings')}[/bold green]")
    cm = ConfigManager()

    # Load current settings
    settings = cm.load_settings()
    current_telemetry = settings.get("telemetry:enabled", True)

    while True:
        # Show menu
        choice = questionary.select(
            t("Select Setting to Configure:"),
            choices=[
                questionary.Choice(title=f"{t('Telemetry Enabled')}: {current_telemetry}", value="telemetry"),
                questionary.Separator(),
                questionary.Choice(title=t("Go Back"), value="back")
            ]
        ).ask()

        if choice == "back":
            break

        elif choice == "telemetry":
            new_val = questionary.confirm(
                t("Enable Telemetry?"),
                default=current_telemetry
            ).ask()
            cm.set_config_value("telemetry:enabled", new_val)
            current_telemetry = new_val
            console.print(f"[green]{t('Updated telemetry setting.')}[/green]")
