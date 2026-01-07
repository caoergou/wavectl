import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_theme():
    console.print(f"[bold green]{t('Configure Theme')}[/bold green]")

    while True:
        choice = questionary.select(
            t("What would you like to do?"),
            choices=[
                questionary.Choice(t("Set Global Terminal Theme"), value="global"),
                questionary.Choice(t("Create Background Preset"), value="create_preset"),
                questionary.Choice(t("Go Back"), value="back")
            ]
        ).ask()

        if choice == "back":
            break
        elif choice == "global":
            _configure_global_theme()
        elif choice == "create_preset":
            _create_background_preset_wizard()

def _configure_global_theme():
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

def _create_background_preset_wizard():
    console.print(f"[bold]{t('Create Background Preset')}[/bold]")

    name = questionary.text(t("Preset Name (e.g. My Red):")).ask()
    if not name:
        return

    # Helper to sanitize key? Usually user provides it.
    key = questionary.text(t("Preset Key (e.g. myred):")).ask()
    if not key:
        return

    bg_type = questionary.select(
        t("Background Type:"),
        choices=[
            questionary.Choice(t("Solid Color"), value="Solid Color"),
            questionary.Choice(t("Gradient"), value="Gradient"),
            questionary.Choice(t("Image"), value="Image")
        ]
    ).ask()

    bg_value = ""
    if bg_type == "Solid Color":
        bg_value = questionary.text(t("Color (hex/rgba, e.g. #ff0000):")).ask()
    elif bg_type == "Gradient":
        bg_value = questionary.text(t("Gradient CSS (e.g. linear-gradient(...)):")).ask()
    elif bg_type == "Image":
        path = questionary.text(t("Image Path (absolute or starting with ~):")).ask()
        if path:
            # Escape single quotes in path to ensure valid CSS URL syntax
            escaped_path = path.replace("'", "\\'")
            bg_value = f"url('{escaped_path}') no-repeat center/cover"

    opacity_str = questionary.text(t("Opacity (0.0 - 1.0, default 0.5):"), default="0.5").ask()
    try:
        opacity = float(opacity_str)
    except ValueError:
        opacity = 0.5

    preset_data = {
        "display:name": name,
        "bg:*": True,
        "bg": bg_value,
        "bg:opacity": opacity
    }

    # Save to presets/bg.json
    full_key = f"bg@{key}"
    cm = ConfigManager()
    cm.update_preset("bg.json", full_key, preset_data)

    console.print(f"[green]{t('Successfully created background preset \'{name}\' ({full_key})', name=name, full_key=full_key)}[/green]")
