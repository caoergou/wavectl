import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t

console = Console()

def configure_ssh_connections():
    console.print(f"[bold green]{t('Configure SSH Connections')}[/bold green]")

    while True:
        action = questionary.select(
            t("What would you like to do?"),
            choices=[
                questionary.Choice(title=t("Add New SSH Connection"), value="Add New SSH Connection"),
                questionary.Choice(title=t("Go Back"), value="Go Back")
            ]
        ).ask()

        if action == "Go Back":
            break

        if action == "Add New SSH Connection":
            add_ssh_connection()

def add_ssh_connection():
    # 1. Gather SSH Details
    # We can use an alias or just user@host

    hostname = questionary.text(t("Enter Hostname or IP (Required):")).ask()
    while not hostname:
         console.print(f"[red]{t('Hostname is required.')}[/red]")
         hostname = questionary.text(t("Enter Hostname or IP (Required):")).ask()

    username = questionary.text(t("Enter Username:"), default="root").ask()
    port = questionary.text(t("Enter Port:"), default="22").ask()

    # Optional: Identity File
    use_key = questionary.confirm(t("Do you use an identity file (private key)?")).ask()
    identity_file = []
    if use_key:
        path = questionary.path(t("Path to private key:"), default="~/.ssh/id_rsa").ask()
        if path:
            identity_file.append(path)

    # 2. Construct Data
    # Key in connections.json is usually "user@hostname" or a custom label.
    # If we want it to appear in the dropdown as a specific entry, we can key it.
    # Docs say: "manual typing... will be added to internal config/connections.json file"
    # Docs example: "myusername@myhost": { "term:theme": ... }
    # Also "Entirely Defined Internally":
    # "myusername@myhost" : { "ssh:hostname": "...", "ssh:identityfile": [...] }

    # Let's ask for a display alias (optional)
    alias = questionary.text(t("Enter a Display Name (Alias) [Optional]:")).ask()

    if alias:
        connection_key = alias
    else:
        connection_key = f"{username}@{hostname}"
        if port and port != "22":
            connection_key += f":{port}"

    connection_data = {
        "ssh:hostname": hostname,
        "ssh:user": username,
    }

    if port and port != "22":
        connection_data["ssh:port"] = port

    if identity_file:
        connection_data["ssh:identityfile"] = identity_file

    # 3. Save
    cm = ConfigManager()
    cm.update_connection(connection_key, connection_data)

    console.print(f"[green]{t('Successfully saved SSH connection \'{connection_key}\' to ~/.config/waveterm/connections.json', connection_key=connection_key)}[/green]")
