import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

RECOMMENDED_PRESETS = {
    "bg@default": {
        "display:name": "Default",
        "display:order": -1,
        "bg:*": True
    },
    "bg@rainbow": {
        "display:name": "Rainbow",
        "display:order": 2.1,
        "bg:*": True,
        "bg": "linear-gradient( 226.4deg,  rgba(255,26,1,1) 28.9%, rgba(254,155,1,1) 33%, rgba(255,241,0,1) 48.6%, rgba(34,218,1,1) 65.3%, rgba(0,141,254,1) 80.6%, rgba(113,63,254,1) 100.1% )",
        "bg:opacity": 0.3
    },
    "bg@green": {
        "display:name": "Green",
        "display:order": 1.2,
        "bg:*": True,
        "bg": "green",
        "bg:opacity": 0.3
    },
    "bg@blue": {
        "display:name": "Blue",
        "display:order": 1.1,
        "bg:*": True,
        "bg": "blue",
        "bg:opacity": 0.3,
        "bg:activebordercolor": "rgba(0, 0, 255, 1.0)"
    },
    "bg@red": {
        "display:name": "Red",
        "display:order": 1.3,
        "bg:*": True,
        "bg": "red",
        "bg:opacity": 0.3,
        "bg:activebordercolor": "rgba(255, 0, 0, 1.0)"
    },
    "bg@ocean-depths": {
        "display:name": "Ocean Depths",
        "display:order": 2.2,
        "bg:*": True,
        "bg": "linear-gradient(135deg, purple, blue, teal)",
        "bg:opacity": 0.7
    },
    "bg@aqua-horizon": {
        "display:name": "Aqua Horizon",
        "display:order": 2.3,
        "bg:*": True,
        "bg": "linear-gradient(135deg, rgba(15, 30, 50, 1) 0%, rgba(40, 90, 130, 0.85) 30%, rgba(20, 100, 150, 0.75) 60%, rgba(0, 120, 160, 0.65) 80%, rgba(0, 140, 180, 0.55) 100%), linear-gradient(135deg, rgba(100, 80, 255, 0.4), rgba(0, 180, 220, 0.4)), radial-gradient(circle at 70% 70%, rgba(255, 255, 255, 0.05), transparent 70%)",
        "bg:opacity": 0.85,
        "bg:blendmode": "overlay"
    },
    "bg@sunset": {
        "display:name": "Sunset",
        "display:order": 2.4,
        "bg:*": True,
        "bg": "linear-gradient(135deg, rgba(128, 0, 0, 1), rgba(255, 69, 0, 0.8), rgba(75, 0, 130, 1))",
        "bg:opacity": 0.8,
        "bg:blendmode": "normal"
    },
    "bg@enchantedforest": {
        "display:name": "Enchanted Forest",
        "display:order": 2.7,
        "bg:*": True,
        "bg": "linear-gradient(145deg, rgba(0,50,0,1), rgba(34,139,34,0.7) 20%, rgba(0,100,0,0.5) 40%, rgba(0,200,100,0.3) 60%, rgba(34,139,34,0.8) 80%, rgba(0,50,0,1)), radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), transparent 80%), radial-gradient(circle at 70% 70%, rgba(255,255,255,0.1), transparent 80%)",
        "bg:opacity": 0.8,
        "bg:blendmode": "soft-light"
    },
    "bg@twilight-mist": {
        "display:name": "Twilight Mist",
        "display:order": 2.9,
        "bg:*": True,
        "bg": "linear-gradient(180deg, rgba(60,60,90,1) 0%, rgba(90,110,140,0.8) 40%, rgba(120,140,160,0.6) 70%, rgba(60,60,90,1) 100%), radial-gradient(circle at 30% 40%, rgba(255,255,255,0.15), transparent 60%), radial-gradient(circle at 70% 70%, rgba(255,255,255,0.1), transparent 70%)",
        "bg:opacity": 0.9,
        "bg:blendmode": "soft-light"
    },
    "bg@duskhorizon": {
        "display:name": "Dusk Horizon",
        "display:order": 3.1,
        "bg:*": True,
        "bg": "linear-gradient(0deg, rgba(128,0,0,1) 0%, rgba(204,85,0,0.7) 20%, rgba(255,140,0,0.6) 45%, rgba(160,90,160,0.5) 65%, rgba(60,60,120,1) 100%), radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), transparent 60%), radial-gradient(circle at 70% 70%, rgba(255,255,255,0.05), transparent 70%)",
        "bg:opacity": 0.9,
        "bg:blendmode": "overlay"
    },
    "bg@tropical-radiance": {
        "display:name": "Tropical Radiance",
        "display:order": 3.3,
        "bg:*": True,
        "bg": "linear-gradient(135deg, rgba(204, 51, 255, 0.9) 0%, rgba(255, 85, 153, 0.75) 30%, rgba(255, 51, 153, 0.65) 60%, rgba(204, 51, 255, 0.6) 80%, rgba(51, 102, 255, 0.5) 100%), radial-gradient(circle at 30% 40%, rgba(255,255,255,0.1), transparent 60%), radial-gradient(circle at 70% 70%, rgba(255,255,255,0.05), transparent 70%)",
        "bg:opacity": 0.9,
        "bg:blendmode": "overlay"
    },
    "bg@twilight-ember": {
        "display:name": "Twilight Ember",
        "display:order": 3.5,
        "bg:*": True,
        "bg": "linear-gradient(120deg,hsla(350, 65%, 57%, 1),hsla(30,60%,60%, .75), hsla(208,69%,50%,.15), hsl(230,60%,40%)),radial-gradient(at top right,hsla(300,60%,70%,0.3),transparent),radial-gradient(at top left,hsla(330,100%,70%,.20),transparent),radial-gradient(at top right,hsla(190,100%,40%,.20),transparent),radial-gradient(at bottom left,hsla(323,54%,50%,.5),transparent),radial-gradient(at bottom left,hsla(144,54%,50%,.25),transparent)",
        "bg:blendmode": "overlay",
        "bg:text": "rgb(200, 200, 200)"
    },
    "bg@cosmic-tide": {
        "display:name": "Cosmic Tide",
        "display:order": 3.6,
        "bg:activebordercolor": "#ff55aa",
        "bg:*": True,
        "bg": "linear-gradient(135deg, #00d9d9, #ff55aa, #1e1e2f, #2f3b57, #ff99ff)",
        "bg:opacity": 0.6
    }
}

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
    # Offer recommended presets
    choices = [questionary.Choice(t("Enter Custom Key..."), value="custom")]
    for key, data in RECOMMENDED_PRESETS.items():
        choices.append(questionary.Choice(title=t(data.get("display:name", key)), value=key))
    choices.append(questionary.Choice(t("Go Back"), value="back"))

    preset_choice = questionary.select(
        t("Select a Default Tab Theme:"),
        choices=choices
    ).ask()

    if not preset_choice or preset_choice == "back":
        return

    preset_key = ""
    cm = ConfigManager()

    if preset_choice == "custom":
        preset_key = questionary.text(t("Enter Tab Preset Key (e.g. bg@myred):")).ask()
        if not preset_key:
            return
    else:
        # Recommended preset selected
        preset_key = preset_choice
        preset_data = RECOMMENDED_PRESETS[preset_key]
        # Save/Ensure the preset exists in bg.json
        cm.update_preset("bg.json", preset_key, preset_data)
        console.print(f"[green]{t('Ensured preset \'{preset_key}\' exists in configuration.', preset_key=preset_key)}[/green]")

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
