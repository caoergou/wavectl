import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_widgets():
    console.print(f"[bold green]{t('Configure Widgets')}[/bold green]")

    # Default widgets in WaveTerm
    # We want to allow enabling/disabling them.
    # Disabling means setting them to null in widgets.json.
    # Enabling means removing the null override (or not having it).

    default_widgets = [
        ("Terminal", "defwidget@terminal"),
        ("Files", "defwidget@files"),
        ("Web", "defwidget@web"),
        ("AI", "defwidget@ai"),
        ("Sysinfo", "defwidget@sysinfo"),
    ]

    cm = ConfigManager()
    current_widgets_config = cm.load_widgets()

    # Determine current state
    # If key is missing or not null -> Enabled (Checked)
    # If key is present and null -> Disabled (Unchecked)

    final_choices = []

    for label, key in default_widgets:
        is_enabled = True

        # We need to distinguish between "key missing" and "key is null".
        if key in current_widgets_config and current_widgets_config[key] is None:
            # Explicitly disabled
            is_enabled = False

        # Create choice with translated label
        final_choices.append(questionary.Choice(title=t(label), value=key, checked=is_enabled))

    selected_keys = questionary.checkbox(
        t("Select active default widgets:"),
        choices=final_choices
    ).ask()

    if selected_keys is None:
        return

    # Process changes
    for label, key in default_widgets:
        if key in selected_keys:
            # User wants it ENABLED.
            # Ensure it is NOT null in config.
            # If it was null, remove the override.
            if key in current_widgets_config and current_widgets_config[key] is None:
                cm.remove_widget_override(key)
        else:
            # User wants it DISABLED.
            # Set to null in config.
            cm.update_widget(key, None)

    console.print(f"[green]{t('Successfully updated active widgets.')}[/green]")
