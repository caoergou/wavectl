import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_ai_settings():
    console.print("[bold green]Configure AI Settings[/bold green]")

    # 1. Select Provider
    provider = questionary.select(
        "Select AI Provider:",
        choices=[
            "OpenAI",
            "Anthropic (Claude)",
            "Ollama (Local)",
            "Go Back"
        ]
    ).ask()

    if provider == "Go Back":
        return

    # 2. Gather details based on provider
    api_token = ""
    model = ""
    api_type = ""

    if provider == "OpenAI":
        api_type = "openai"
        model = questionary.text("Enter Model Name (e.g., gpt-4, gpt-3.5-turbo):", default="gpt-4").ask()
        api_token = questionary.password("Enter OpenAI API Key:").ask()
        preset_prefix = "openai"

    elif provider == "Anthropic (Claude)":
        api_type = "anthropic"
        model = questionary.text("Enter Model Name (e.g., claude-3-5-sonnet-latest):", default="claude-3-5-sonnet-latest").ask()
        api_token = questionary.password("Enter Anthropic API Key:").ask()
        preset_prefix = "claude"

    elif provider == "Ollama (Local)":
        # For Ollama, the structure might be slightly different or rely on a compatible endpoint
        # Based on docs, it usually acts as an openai compatible endpoint or has specific config
        # Assuming generic setup or verifying docs if needed.
        # For now, let's treat it as a custom setup or skip specific api_type if not strictly documented for simple "ollama" key
        # However, the user wants me to implement logic.
        # Docs example: "ai@ollama-llama": { ... }
        # Let's assume standard fields.
        api_type = "openai" # often used for local servers mimicking openai
        model = questionary.text("Enter Ollama Model Name (e.g., llama2):", default="llama2").ask()
        api_token = "unused" # Ollama often doesn't need a key
        preset_prefix = "ollama"

        # Check if user needs to specify a custom base URL
        custom_url = questionary.confirm("Do you need to specify a custom Base URL? (Default is usually http://localhost:11434/v1)").ask()
        if custom_url:
            base_url = questionary.text("Enter Base URL:", default="http://localhost:11434/v1").ask()
        else:
            base_url = "http://localhost:11434/v1"

    # 3. Define Preset Name
    preset_name_input = questionary.text(
        "Enter a name for this preset (display name):",
        default=f"{provider} - {model}"
    ).ask()

    # Generate a unique key for the preset
    # Standard format: ai@<unique-id>
    # We'll use a sanitized version of the display name or just a timestamp/random string if needed.
    # Let's use a sanitized version of the model + provider.
    sanitized_name = f"{preset_prefix}-{model}".replace(" ", "-").replace(".", "").lower()
    preset_key = f"ai@{sanitized_name}"

    # 4. Construct the preset data
    preset_data = {
        "display:name": preset_name_input,
        "display:order": 1, # TODO: Logic to auto-increment order?
        "ai:*": True, # Reset other AI settings
        "ai:model": model,
    }

    if provider != "Ollama (Local)":
        preset_data["ai:apitype"] = api_type
        preset_data["ai:apitoken"] = api_token
    else:
        # specific for local/ollama if needed
        preset_data["ai:baseurl"] = base_url
        preset_data["ai:apitype"] = "openai" # Ollama compatible
        preset_data["ai:apitoken"] = "ollama" # placeholder

    # 5. Save to Config
    cm = ConfigManager()
    cm.update_preset("ai.json", preset_key, preset_data)

    console.print(f"[green]Successfully saved preset '{preset_name_input}' to ~/.config/waveterm/presets/ai.json[/green]")

    # 6. Ask to set as default
    set_default = questionary.confirm("Do you want to set this as your default AI preset?").ask()
    if set_default:
        cm.set_config_value("ai:preset", preset_key)
        console.print(f"[green]Set '{preset_name_input}' as the default AI preset.[/green]")
