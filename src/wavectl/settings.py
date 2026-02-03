import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t, set_language, get_language

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
                questionary.Choice(title=_get_title("term:fontsize", t("Terminal Font Size"), t("Default")), value="termfontsize"),
                questionary.Choice(title=_get_title("term:scrollback", t("Terminal Scrollback"), -1), value="scrollback"),
                questionary.Choice(title=_get_title("term:copyonselect", t("Copy on Select"), True), value="copyonselect"),
                questionary.Choice(title=_get_title("window:confirmclose", t("Confirm Window Close"), True), value="confirmclose"),
                questionary.Choice(title=_get_title("window:savelastwindow", t("Save Last Window State"), True), value="savelastwindow"),
                questionary.Choice(title=_get_title("app:showoverlayblocknums", t("Show Block Numbers Overlay"), True), value="showoverlayblocknums"),
                questionary.Choice(title=_get_title("term:shiftenternewline", t("Shift+Enter for Newline"), True), value="shiftenternewline"),
                questionary.Choice(title=_get_title("preview:showhiddenfiles", t("Show Hidden Files in Preview"), False), value="showhiddenfiles"),
                questionary.Choice(title=_get_title("window:nativetitlebar", t("Use Native Title Bar"), False), value="nativetitlebar"),
                questionary.Choice(title=_get_title("term:macoptionismeta", t("Use Option as Meta (MacOS)"), False), value="macoptionismeta"),
                questionary.Choice(title=_get_title("term:transparency", t("Terminal Transparency"), 1.0), value="transparency"),
                questionary.Choice(title=_get_title("window:disablehardwareacceleration", t("Disable Hardware Acceleration"), False), value="disablehardwareacceleration"),
                questionary.Choice(title=_get_title("term:allowbracketedpaste", t("Allow Bracketed Paste"), True), value="allowbracketedpaste"),
                questionary.Choice(title=_get_title("editor:wordwrap", t("Editor Word Wrap"), False), value="editorwordwrap"),
                questionary.Choice(title=_get_title("web:homedefault", t("Default Web Home URL"), ""), value="webhomedefault"),
                questionary.Choice(title=f"{t('Language')}: {get_language()}", value="language"),
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

        elif choice == "termfontsize":
            curr = str(settings.get("term:fontsize", ""))
            new_val_str = questionary.text(t("Enter Terminal Font Size (int, 0/empty to default):"), default=curr).ask()
            if not new_val_str.strip() or new_val_str.strip() == "0":
                 cm.set_config_value("term:fontsize", None)
                 console.print(f"[green]{t('Reset terminal font size to default.')}[/green]")
            else:
                 try:
                     val = int(new_val_str)
                     cm.set_config_value("term:fontsize", val)
                     console.print(f"[green]{t('Updated terminal font size.')}[/green]")
                 except ValueError:
                     console.print(f"[red]{t('Invalid integer.')}[/red]")

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

        elif choice == "transparency":
            curr = settings.get("term:transparency", 1.0)
            new_val_str = questionary.text(t("Enter Transparency (0.0 to 1.0):"), default=str(curr)).ask()
            try:
                val = float(new_val_str)
                if val < 0.0 or val > 1.0:
                    console.print(f"[red]{t('Value must be between 0.0 and 1.0')}[/red]")
                else:
                    cm.set_config_value("term:transparency", val)
                    console.print(f"[green]{t('Updated transparency setting.')}[/green]")
            except ValueError:
                console.print(f"[red]{t('Invalid float.')}[/red]")

        elif choice == "disablehardwareacceleration":
            curr = settings.get("window:disablehardwareacceleration", False)
            new_val = questionary.confirm(t("Disable Hardware Acceleration?"), default=curr).ask()
            cm.set_config_value("window:disablehardwareacceleration", new_val)
            console.print(f"[green]{t('Updated hardware acceleration setting.')}[/green]")

        elif choice == "allowbracketedpaste":
            curr = settings.get("term:allowbracketedpaste", True)
            new_val = questionary.confirm(t("Allow Bracketed Paste?"), default=curr).ask()
            cm.set_config_value("term:allowbracketedpaste", new_val)
            console.print(f"[green]{t('Updated bracketed paste setting.')}[/green]")

        elif choice == "editorwordwrap":
            curr = settings.get("editor:wordwrap", False)
            new_val = questionary.confirm(t("Enable Editor Word Wrap?"), default=curr).ask()
            cm.set_config_value("editor:wordwrap", new_val)
            console.print(f"[green]{t('Updated editor word wrap setting.')}[/green]")

        elif choice == "webhomedefault":
            curr = settings.get("web:homedefault", "")
            new_val = questionary.text(t("Enter Default Web Home URL (empty to remove):"), default=curr).ask()
            if new_val.strip() == "":
                cm.set_config_value("web:homedefault", None)
                console.print(f"[green]{t('Removed default web home URL.')}[/green]")
            else:
                cm.set_config_value("web:homedefault", new_val)
                console.print(f"[green]{t('Updated default web home URL.')}[/green]")

        elif choice == "language":
            lang_choice = questionary.select(
                t("Select Language:"),
                choices=[
                    questionary.Choice(title="English", value="en_US"),
                    questionary.Choice(title="中文", value="zh_CN")
                ],
                default=get_language()
            ).ask()
            if lang_choice:
                set_language(lang_choice)
                console.print(f"[green]{t('Language updated.')}[/green]")
