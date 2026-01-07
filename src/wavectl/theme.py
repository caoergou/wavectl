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
                questionary.Choice(t("Set Terminal Font Size"), value="font_size"),
                questionary.Choice(t("Set Terminal Font Family"), value="font_family"),
                questionary.Choice(t("Set Default Tab Theme"), value="tab_preset"),
                questionary.Choice(t("Toggle Help Widget"), value="help_widget"),
                questionary.Choice(t("Create Background Preset"), value="create_preset"),
                questionary.Choice(t("Go Back"), value="back")
            ]
        ).ask()

        if choice is None or choice == "back":
            break
        elif choice == "global":
            _configure_global_theme()
        elif choice == "font_size":
            _configure_font_size()
        elif choice == "font_family":
            _configure_font_family()
        elif choice == "tab_preset":
            _configure_tab_preset()
        elif choice == "help_widget":
            _toggle_help_widget()
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

    if not choice or choice == "Go Back":
        return

    theme_value = themes[choice]

    cm = ConfigManager()

    # Set global theme in settings.json
    # Key: term:theme
    cm.set_config_value("term:theme", theme_value)

    console.print(f"[green]{t('Successfully set global theme to \'{choice}\' ({theme_value})', choice=choice, theme_value=theme_value)}[/green]")

def _configure_font_size():
    size_str = questionary.text(t("Enter Font Size (e.g. 14):")).ask()
    if not size_str:
        return

    try:
        size = int(size_str)
        cm = ConfigManager()
        cm.set_config_value("term:fontsize", size)
        console.print(f"[green]{t('Successfully set font size to {size}', size=size)}[/green]")
    except ValueError:
        console.print(f"[red]{t('Invalid font size. Please enter a number.')}[/red]")

def _configure_font_family():
    family = questionary.text(t("Enter Font Family (e.g. Fira Code):")).ask()
    if not family:
        return

    cm = ConfigManager()
    cm.set_config_value("term:fontfamily", family)
    console.print(f"[green]{t('Successfully set font family to \'{family}\'', family=family)}[/green]")

def _configure_tab_preset():
    # Built-in presets available in WaveTerm
    builtin_presets = [
        ("Default", "bg@default"),
        ("Rainbow", "bg@rainbow"),
        ("Green", "bg@green"),
        ("Blue", "bg@blue"),
        ("Red", "bg@red"),
        ("Ocean Depths", "bg@ocean-depths"),
        ("Aqua Horizon", "bg@aqua-horizon"),
        ("Sunset", "bg@sunset"),
        ("Enchanted Forest", "bg@enchantedforest"),
        ("Twilight Mist", "bg@twilight-mist"),
        ("Dusk Horizon", "bg@duskhorizon"),
        ("Tropical Radiance", "bg@tropical-radiance"),
        ("Twilight Ember", "bg@twilight-ember"),
        ("Cosmic Tide", "bg@cosmic-tide")
    ]

    choices = [questionary.Choice(t("Enter Custom Key..."), value="custom")]
    for name, key in builtin_presets:
        choices.append(questionary.Choice(title=t(name), value=key))
    choices.append(questionary.Choice(t("Go Back"), value="back"))

    preset_choice = questionary.select(
        t("Select a Default Tab Theme:"),
        choices=choices
    ).ask()

    if not preset_choice or preset_choice == "back":
        return

    preset_key = ""

    if preset_choice == "custom":
        preset_key = questionary.text(t("Enter Tab Preset Key (e.g. bg@myred):")).ask()
        if not preset_key:
            return
    else:
        # Built-in preset selected
        preset_key = preset_choice

    cm = ConfigManager()
    # Set as default
    cm.set_config_value("tab:preset", preset_key)
    console.print(f"[green]{t('Successfully set default tab preset to \'{preset_key}\'', preset_key=preset_key)}[/green]")

def _toggle_help_widget():
    choice = questionary.select(
        t("Help Widget Visibility:"),
        choices=[
            questionary.Choice(t("Show"), value="show"),
            questionary.Choice(t("Hide"), value="hide")
        ]
    ).ask()

    if not choice:
        return

    cm = ConfigManager()
    if choice == "show":
        cm.set_config_value("widget:showhelp", True)
        console.print(f"[green]{t('Help widget enabled.')}[/green]")
    elif choice == "hide":
        cm.set_config_value("widget:showhelp", False)
        console.print(f"[green]{t('Help widget disabled.')}[/green]")

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

    if not bg_type:
        return

    bg_value = ""
    if bg_type == "Solid Color":
        bg_value = questionary.text(t("Color (hex/rgba, e.g. #ff0000):")).ask()
    elif bg_type == "Gradient":
        bg_value = questionary.text(t("Gradient CSS (e.g. linear-gradient(...)):")).ask()
    elif bg_type == "Image":
        path = questionary.text(t("Image Path (absolute or starting with ~):")).ask()
        if path:
            # Escape single quotes and backslashes for CSS URL compatibility
            # Replace backslashes with forward slashes is generally safer for CSS URLs across platforms
            # And escape single quotes
            safe_path = path.replace("\\", "/").replace("'", "\\'")
            bg_value = f"url('{safe_path}') no-repeat center/cover"

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
