import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_widgets():
    console.print("[bold green]Configure Widgets[/bold green]")

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

    initial_checked = []
    for label, key in default_widgets:
        if current_widgets_config.get(key) is None:
            # Note: json.load reads null as None.
            # But if key is missing, .get returns None.
            # Wait, if key is missing, it is ENABLED (default).
            # If key is present and is null (None), it is DISABLED.

            # We need to distinguish between "key missing" and "key is null".
            if key in current_widgets_config and current_widgets_config[key] is None:
                # Explicitly disabled
                pass
            else:
                # Enabled
                initial_checked.append(questionary.Choice(label, value=key, checked=True))
        else:
             # If key present and NOT null, it's a custom override, so it's enabled.
             initial_checked.append(questionary.Choice(label, value=key, checked=True))

    # Add disabled ones as unchecked
    for label, key in default_widgets:
        is_enabled = False
        # check if we already added it
        for choice in initial_checked:
            if choice.value == key:
                is_enabled = True
                break

        if not is_enabled:
             initial_checked.append(questionary.Choice(label, value=key, checked=False))

    # Sort them to match default order usually
    # But questionary preserves order of list.
    # Let's rebuild the list in order
    final_choices = []
    for label, key in default_widgets:
        # Find the choice object
        found = next((c for c in initial_checked if c.value == key), None)
        if found:
            final_choices.append(found)

    selected_keys = questionary.checkbox(
        "Select active default widgets:",
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

    console.print(f"[green]Successfully updated active widgets.[/green]")
