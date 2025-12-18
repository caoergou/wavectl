import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_ai_settings():
    console.print("[bold green]Configure AI Modes (waveai.json)[/bold green]")

    # 1. Select Provider
    provider = questionary.select(
        "Select AI Provider:",
        choices=[
            "OpenAI",
            "Ollama (Local)",
            "OpenRouter",
            "Go Back"
        ]
    ).ask()

    if provider == "Go Back":
        return

    mode_data = {}
    mode_key = ""
    display_name = ""

    if provider == "OpenAI":
        display_name = questionary.text("Enter Display Name:", default="OpenAI GPT-4o").ask()
        model = questionary.text("Enter Model Name:", default="gpt-4o").ask()

        # Construct key from model name
        mode_key = f"openai-{model.replace('.', '').replace(':', '-')}"

        mode_data = {
            "display:name": display_name,
            "ai:provider": "openai",
            "ai:model": model
        }

        console.print("[yellow]Note: For OpenAI, please ensure you have set the secret OPENAI_KEY using:[/yellow]")
        console.print("[bold]wsh secret set OPENAI_KEY=sk-xxxxxxxx[/bold]")

    elif provider == "Ollama (Local)":
        display_name = questionary.text("Enter Display Name:", default="Ollama - Llama 3").ask()
        model = questionary.text("Enter Model Name (e.g., llama3:latest):", default="llama3:latest").ask()

        mode_key = f"ollama-{model.replace(':', '-')}"

        mode_data = {
            "display:name": display_name,
            "ai:apitype": "openai-chat",
            "ai:model": model,
            "ai:endpoint": "http://localhost:11434/v1/chat/completions",
            "ai:apitoken": "ollama"
        }

    elif provider == "OpenRouter":
        display_name = questionary.text("Enter Display Name:", default="OpenRouter - Model").ask()
        model = questionary.text("Enter Model Name (e.g., qwen/qwen-2.5-coder-32b-instruct):", default="qwen/qwen-2.5-coder-32b-instruct").ask()

        # Clean up key
        clean_model = model.split("/")[-1].replace('.', '').replace(':', '-')
        mode_key = f"openrouter-{clean_model}"

        mode_data = {
            "display:name": display_name,
            "ai:provider": "openrouter",
            "ai:model": model
        }

        console.print("[yellow]Note: For OpenRouter, please ensure you have set the secret OPENROUTER_KEY using:[/yellow]")
        console.print("[bold]wsh secret set OPENROUTER_KEY=sk-xxxxxxxx[/bold]")

        # Ask for capabilities as per docs for OpenRouter
        # "For OpenRouter, you must manually specify ai:capabilities"
        capabilities = questionary.checkbox(
            "Select Capabilities:",
            choices=["tools", "images", "pdfs"],
            default=["tools"]
        ).ask()
        mode_data["ai:capabilities"] = capabilities

    # Ask for display order
    try:
        order = int(questionary.text("Enter Display Order (number):", default="1").ask())
    except ValueError:
        order = 1
    mode_data["display:order"] = order

    # Save to Config
    cm = ConfigManager()
    cm.update_waveai_mode(mode_key, mode_data)

    console.print(f"[green]Successfully saved mode '{mode_key}' to ~/.config/waveterm/waveai.json[/green]")

    # Ask to set as default
    set_default = questionary.confirm("Do you want to set this as your default AI mode?").ask()
    if set_default:
        cm.set_config_value("waveai:defaultmode", mode_key)
        console.print(f"[green]Set '{mode_key}' as the default AI mode.[/green]")
