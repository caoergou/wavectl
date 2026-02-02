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

    # Optional: Password Secret
    # v0.13: ssh:passwordsecretname
    use_pass_secret = questionary.confirm(t("Do you want to store the SSH password in the secret store?")).ask()
    if use_pass_secret:
        # Sanitize hostname for secret name suggestion
        safe_host = hostname.replace(".", "_").replace("-", "_").upper()
        default_secret_name = f"SSH_PASSWORD_{safe_host}"

        secret_name = questionary.text(
            t("Enter Secret Name for Password:"),
            default=default_secret_name
        ).ask()

        if secret_name:
            connection_data["ssh:passwordsecretname"] = secret_name

            has_secret = questionary.confirm(t(f"Do you have the secret '{secret_name}' set?")).ask()
            if not has_secret:
                password = questionary.password(t("Enter SSH Password (to display setup command):")).ask()
                if password:
                    console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                    console.print(f"wsh secret set {secret_name}={password}")

    # Environment Variables (cmd:env)
    configure_env = questionary.confirm(t("Configure environment variables?")).ask()
    if configure_env:
        env_vars = {}
        while True:
            var_name = questionary.text(t("Enter Variable Name (empty to finish):")).ask()
            if not var_name or not var_name.strip():
                break
            var_value = questionary.text(t("Enter Value for {var}:", var=var_name)).ask()
            env_vars[var_name] = var_value

        if env_vars:
            connection_data["cmd:env"] = env_vars

    # 3. Save
    cm = ConfigManager()
    cm.update_connection(connection_key, connection_data)

    console.print(f"[green]{t('Successfully saved SSH connection \'{connection_key}\' to ~/.config/waveterm/connections.json', connection_key=connection_key)}[/green]")
