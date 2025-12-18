import questionary
from rich.console import Console
from .config_manager import ConfigManager

console = Console()

def configure_ssh_connections():
    console.print("[bold green]Configure SSH Connections[/bold green]")

    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Add New SSH Connection",
                "Go Back"
            ]
        ).ask()

        if action == "Go Back":
            break

        if action == "Add New SSH Connection":
            add_ssh_connection()

def add_ssh_connection():
    # 1. Gather SSH Details
    connection_name = questionary.text("Enter Connection Name (e.g., Production DB):").ask()
    if not connection_name:
        return

    hostname = questionary.text("Enter Hostname or IP:").ask()
    while not hostname:
         console.print("[red]Hostname is required.[/red]")
         hostname = questionary.text("Enter Hostname or IP:").ask()

    username = questionary.text("Enter Username:", default="root").ask()
    port = questionary.text("Enter Port:", default="22").ask()

    # Optional: Identity File
    use_key = questionary.confirm("Do you use an identity file (private key)?").ask()
    identity_file = ""
    if use_key:
        identity_file = questionary.path("Path to private key:", default="~/.ssh/id_rsa").ask()

    # 2. Construct Preset Data
    # Assuming WaveTerm uses a generic 'term' preset for SSH or specific structure.
    # Pattern: term:cmd = ssh ...

    cmd_parts = ["ssh"]
    if port and port != "22":
        cmd_parts.extend(["-p", port])
    if identity_file:
        cmd_parts.extend(["-i", identity_file])

    cmd_parts.append(f"{username}@{hostname}")

    full_cmd = " ".join(cmd_parts)

    # Sanitize key
    sanitized_name = connection_name.replace(" ", "-").replace(".", "").lower()
    preset_key = f"term@ssh-{sanitized_name}"

    preset_data = {
        "display:name": connection_name,
        "term:cmd": full_cmd,
        "term:icon": "server", # heuristic
    }

    # 3. Save
    cm = ConfigManager()
    # Storing in term.json as these are likely terminal presets
    cm.update_preset("term.json", preset_key, preset_data)

    console.print(f"[green]Successfully saved SSH connection '{connection_name}' to ~/.config/waveterm/presets/term.json[/green]")
