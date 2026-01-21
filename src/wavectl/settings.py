import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_general_settings():
    console.print(f"[bold green]{t('Configure General Settings')}[/bold green]")
    cm = ConfigManager()

    while True:
        # Load current settings (refresh loop)
        settings = cm.load_settings()

        # Helper to get current value for display
        def _get_title(key, label, default):
            val = settings.get(key, default)
            return f"{label}: {val}"

        choice = questionary.select(
            t("Select Setting to Configure:"),
            choices=[
                questionary.Choice(title=_get_title("telemetry:enabled", t("Telemetry Enabled"), True), value="telemetry"),
                questionary.Choice(title=_get_title("term:scrollback", t("Terminal Scrollback"), -1), value="scrollback"),
                questionary.Choice(title=_get_title("term:copyonselect", t("Copy on Select"), True), value="copyonselect"),
                questionary.Choice(title=_get_title("window:confirmclose", t("Confirm Window Close"), True), value="confirmclose"),
                questionary.Choice(title=_get_title("window:savelastwindow", t("Save Last Window State"), True), value="savelastwindow"),
                questionary.Choice(title=_get_title("app:showoverlayblocknums", t("Show Block Numbers Overlay"), True), value="showoverlayblocknums"),
                questionary.Choice(title=_get_title("term:shiftenternewline", t("Shift+Enter for Newline"), True), value="shiftenternewline"),
                questionary.Choice(title=_get_title("preview:showhiddenfiles", t("Show Hidden Files in Preview"), False), value="showhiddenfiles"),
                questionary.Choice(title=_get_title("window:nativetitlebar", t("Use Native Title Bar"), False), value="nativetitlebar"),
                questionary.Choice(title=_get_title("term:macoptionismeta", t("MacOS Option as Meta"), False), value="macoptionismeta"),
                questionary.Separator(),
                questionary.Choice(title=t("Go Back"), value="back")
            ]
        ).ask()

        if choice == "back":
            break

        elif choice == "telemetry":
            curr = settings.get("telemetry:enabled", True)
            new_val = questionary.confirm(t("Enable Telemetry?"), default=curr).ask()
            cm.set_config_value("telemetry:enabled", new_val)
            console.print(f"[green]{t('Updated telemetry setting.')}[/green]")

        elif choice == "scrollback":
            curr = settings.get("term:scrollback", -1)
            new_val_str = questionary.text(t("Enter Scrollback Lines (-1 for default, max 50000):"), default=str(curr)).ask()
            try:
                new_val = int(new_val_str)
                if new_val > 50000:
                    console.print(f"[yellow]{t('Value too high, setting to 50000')}[/yellow]")
                    new_val = 50000
                cm.set_config_value("term:scrollback", new_val)
                console.print(f"[green]{t('Updated scrollback setting.')}[/green]")
            except ValueError:
                console.print(f"[red]{t('Invalid integer.')}[/red]")

        elif choice == "copyonselect":
            curr = settings.get("term:copyonselect", True)
            new_val = questionary.confirm(t("Enable Copy on Select?"), default=curr).ask()
            cm.set_config_value("term:copyonselect", new_val)
            console.print(f"[green]{t('Updated copy on select setting.')}[/green]")

        elif choice == "confirmclose":
            curr = settings.get("window:confirmclose", True)
            new_val = questionary.confirm(t("Confirm before closing window?"), default=curr).ask()
            cm.set_config_value("window:confirmclose", new_val)
            console.print(f"[green]{t('Updated confirm close setting.')}[/green]")

        elif choice == "savelastwindow":
            curr = settings.get("window:savelastwindow", True)
            new_val = questionary.confirm(t("Save last window state?"), default=curr).ask()
            cm.set_config_value("window:savelastwindow", new_val)
            console.print(f"[green]{t('Updated save last window setting.')}[/green]")

        elif choice == "showoverlayblocknums":
            curr = settings.get("app:showoverlayblocknums", True)
            new_val = questionary.confirm(t("Show block numbers overlay?"), default=curr).ask()
            cm.set_config_value("app:showoverlayblocknums", new_val)
            console.print(f"[green]{t('Updated overlay block nums setting.')}[/green]")

        elif choice == "shiftenternewline":
            curr = settings.get("term:shiftenternewline", True)
            new_val = questionary.confirm(t("Use Shift+Enter for newline?"), default=curr).ask()
            cm.set_config_value("term:shiftenternewline", new_val)
            console.print(f"[green]{t('Updated Shift+Enter setting.')}[/green]")

        elif choice == "showhiddenfiles":
            curr = settings.get("preview:showhiddenfiles", False)
            new_val = questionary.confirm(t("Show hidden files in preview?"), default=curr).ask()
            cm.set_config_value("preview:showhiddenfiles", new_val)
            console.print(f"[green]{t('Updated show hidden files setting.')}[/green]")

        elif choice == "nativetitlebar":
            curr = settings.get("window:nativetitlebar", False)
            new_val = questionary.confirm(t("Use native title bar?"), default=curr).ask()
            cm.set_config_value("window:nativetitlebar", new_val)
            console.print(f"[green]{t('Updated native title bar setting.')}[/green]")

        elif choice == "macoptionismeta":
            curr = settings.get("term:macoptionismeta", False)
            new_val = questionary.confirm(t("Treat Option key as Meta on MacOS?"), default=curr).ask()
            cm.set_config_value("term:macoptionismeta", new_val)
            console.print(f"[green]{t('Updated MacOS Option as Meta setting.')}[/green]")
