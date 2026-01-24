import questionary
from rich.console import Console
from .config_manager import ConfigManager
from .i18n import t
import re

console = Console()

def configure_ai_settings():
    console.print(f"[bold green]{t('Configure AI Settings')}[/bold green]")

    while True:
        choice = questionary.select(
            t("Select Action:"),
            choices=[
                questionary.Choice(title=t("Add New AI Mode"), value="add"),
                questionary.Choice(title=t("Global AI Settings"), value="global"),
                questionary.Separator(),
                questionary.Choice(title=t("Go Back"), value="back")
            ]
        ).ask()

        if choice == "back":
            break
        elif choice == "add":
            add_ai_mode()
        elif choice == "global":
            configure_global_ai_settings()

def configure_global_ai_settings():
    console.print(f"[bold blue]{t('Global AI Settings')}[/bold blue]")
    cm = ConfigManager()

    # 1. Default Mode
    modes = cm.load_waveai()
    if not modes:
        console.print(f"[yellow]{t('No AI modes found. Please add a mode first.')}[/yellow]")
    else:
        current_settings = cm.load_settings()
        current_default = current_settings.get("waveai:defaultmode", "")

        choices = []
        for key, data in modes.items():
             name = data.get("display:name", key)
             title = f"{name} ({key})"
             if key == current_default:
                 title += " [Current Default]"
             choices.append(questionary.Choice(title=title, value=key))

        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title=t("Skip / Keep Current"), value="skip"))

        default_mode = questionary.select(
            t("Select Default AI Mode:"),
            choices=choices
        ).ask()

        if default_mode and default_mode != "skip":
             cm.set_config_value("waveai:defaultmode", default_mode)
             console.print(f"[green]{t('Set \'{default_mode}\' as the default AI mode.')}[/green]")

    # 2. Show Cloud Modes
    current_settings = cm.load_settings()
    # If key is missing, default is True (show clouds)
    current_show = current_settings.get("waveai:showcloudmodes", True)

    action = questionary.select(
        t("Show Built-in Cloud Modes (OpenAI, Anthropic, etc.)?"),
        choices=[
            questionary.Choice(title=t("Show Cloud Modes"), value=True),
            questionary.Choice(title=t("Hide Cloud Modes"), value=False),
            questionary.Choice(title=t("Keep Current ({val})", val=current_show), value="skip")
        ],
        default=current_show
    ).ask()

    if action != "skip":
         cm.set_config_value("waveai:showcloudmodes", action)

    # 3. AI Proxy URL
    current_proxy = current_settings.get("ai:proxyurl", "")
    proxy_choice = questionary.confirm(t("Configure Global AI Proxy URL?"), default=bool(current_proxy)).ask()
    if proxy_choice:
        proxy_url = questionary.text(t("Enter Proxy URL (e.g., http://user:pass@host:port):"), default=current_proxy).ask()
        cm.set_config_value("ai:proxyurl", proxy_url)

    # 4. AI Font Size
    current_font = current_settings.get("ai:fontsize", 14)
    font_choice = questionary.confirm(t("Configure Global AI Font Size?"), default=False).ask()
    if font_choice:
        font_size_str = questionary.text(t("Enter Font Size (int):"), default=str(current_font)).ask()
        try:
             font_size = int(font_size_str)
             cm.set_config_value("ai:fontsize", font_size)
        except ValueError:
             console.print(f"[red]{t('Invalid integer.')}[/red]")

    # 5. AI Fixed Font Size
    current_fixed_font = current_settings.get("ai:fixedfontsize", 14)
    fixed_font_choice = questionary.confirm(t("Configure Global AI Fixed Font Size?"), default=False).ask()
    if fixed_font_choice:
        fixed_font_size_str = questionary.text(t("Enter Fixed Font Size (int):"), default=str(current_fixed_font)).ask()
        try:
             fixed_font_size = int(fixed_font_size_str)
             cm.set_config_value("ai:fixedfontsize", fixed_font_size)
        except ValueError:
             console.print(f"[red]{t('Invalid integer.')}[/red]")

    console.print(f"[green]{t('Updated global AI settings.')}[/green]")


def add_ai_mode():
    # 1. Select Provider
    provider = questionary.select(
        t("Select AI Provider:"),
        choices=[
            questionary.Choice(title=t("OpenAI"), value="openai"),
            questionary.Choice(title=t("OpenRouter"), value="openrouter"),
            questionary.Choice(title=t("Google (Gemini)"), value="google"),
            questionary.Choice(title=t("Azure OpenAI"), value="azure"),
            questionary.Choice(title=t("Azure OpenAI (Legacy)"), value="azure-legacy"),
            questionary.Choice(title=t("Custom / Local (Ollama, etc.)"), value="custom"),
            questionary.Separator(),
            questionary.Choice(title=t("Go Back"), value="back")
        ]
    ).ask()

    if provider == "back":
        return

    # 2. Gather Provider Specific Details
    mode_data = {}

    # Common fields that might be asked later or derived
    display_name = ""
    model = ""

    if provider == "openai":
        display_name = questionary.text(t("Enter Display Name:"), default="OpenAI GPT-5.2").ask()
        model = questionary.text(t("Enter Model Name:"), default="gpt-5.2").ask()

        mode_data["ai:provider"] = "openai"
        mode_data["ai:model"] = model

        # Secrets handling
        console.print(f"[yellow]{t('Note: OpenAI provider uses the secret named OPENAI_KEY.')}[/yellow]")
        has_key = questionary.confirm(t("Do you have this secret set?")).ask()
        if not has_key:
            api_key = questionary.password(t("Enter your OpenAI API Key (to display setup command):")).ask()
            if api_key:
                console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                console.print(f"wsh secret set OPENAI_KEY={api_key}")
                console.print(t("(You can do this after finishing this configuration)"))

    elif provider == "openrouter":
        display_name = questionary.text(t("Enter Display Name:"), default="OpenRouter").ask()
        model = questionary.text(t("Enter Model Name (e.g. anthropic/claude-sonnet-4.5):"), default="anthropic/claude-sonnet-4.5").ask()

        mode_data["ai:provider"] = "openrouter"
        mode_data["ai:model"] = model

        # Secrets handling
        console.print(f"[yellow]{t('Note: OpenRouter provider uses the secret named OPENROUTER_KEY.')}[/yellow]")
        has_key = questionary.confirm(t("Do you have this secret set?")).ask()
        if not has_key:
            api_key = questionary.password(t("Enter your OpenRouter API Key (to display setup command):")).ask()
            if api_key:
                console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                console.print(f"wsh secret set OPENROUTER_KEY={api_key}")

        # Capabilities
        # Docs say OpenRouter needs manual capabilities
        mode_data["ai:capabilities"] = _ask_capabilities()

    elif provider == "google":
        display_name = questionary.text(t("Enter Display Name:"), default="Google Gemini").ask()
        model = questionary.text(t("Enter Model Name:"), default="gemini-3-pro-preview").ask()

        mode_data["ai:provider"] = "google"
        mode_data["ai:model"] = model

        # Secrets handling
        console.print(f"[yellow]{t('Note: Google provider uses the secret named GOOGLE_AI_KEY.')}[/yellow]")
        has_key = questionary.confirm(t("Do you have this secret set?")).ask()
        if not has_key:
            api_key = questionary.password(t("Enter your Google AI API Key (to display setup command):")).ask()
            if api_key:
                console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                console.print(f"wsh secret set GOOGLE_AI_KEY={api_key}")

    elif provider == "azure":
        display_name = questionary.text(t("Enter Display Name:"), default="Azure OpenAI").ask()
        resource_name = questionary.text(t("Enter Azure Resource Name:")).ask()
        model = questionary.text(t("Enter Model Name:")).ask()

        mode_data["ai:provider"] = "azure"
        mode_data["ai:model"] = model
        mode_data["ai:azureresourcename"] = resource_name

        # Secrets handling
        console.print(f"[yellow]{t('Note: Azure provider uses the secret named AZURE_OPENAI_KEY.')}[/yellow]")
        has_key = questionary.confirm(t("Do you have this secret set?")).ask()
        if not has_key:
            api_key = questionary.password(t("Enter your Azure OpenAI API Key (to display setup command):")).ask()
            if api_key:
                console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                console.print(f"wsh secret set AZURE_OPENAI_KEY={api_key}")

        # Capabilities
        mode_data["ai:capabilities"] = _ask_capabilities()

    elif provider == "azure-legacy":
        display_name = questionary.text(t("Enter Display Name:"), default="Azure OpenAI (Legacy)").ask()
        resource_name = questionary.text(t("Enter Azure Resource Name:")).ask()
        deployment_name = questionary.text(t("Enter Azure Deployment Name:")).ask()

        mode_data["ai:provider"] = "azure-legacy"
        mode_data["ai:azureresourcename"] = resource_name
        mode_data["ai:azuredeployment"] = deployment_name

        # Optional: API Version
        api_version = questionary.text(t("Enter API Version (optional, default: 2025-04-01-preview):"), default="").ask()
        if api_version:
             mode_data["ai:azureapiversion"] = api_version

        # Secrets handling
        console.print(f"[yellow]{t('Note: For Azure Legacy, you should store your API key in a secret.')}[/yellow]")
        secret_name = questionary.text(t("Enter Secret Name for API Key (default: AZURE_OPENAI_KEY):"), default="AZURE_OPENAI_KEY").ask()
        mode_data["ai:apitokensecretname"] = secret_name

        has_key = questionary.confirm(t(f"Do you have the secret '{secret_name}' set?")).ask()
        if not has_key:
            api_key = questionary.password(t("Enter your Azure API Key (to display setup command):")).ask()
            if api_key:
                 console.print(f"[bold cyan]{t('Please run the following command to set your secret:')}[/bold cyan]")
                 console.print(f"wsh secret set {secret_name}={api_key}")

        # Capabilities
        mode_data["ai:capabilities"] = _ask_capabilities()

    elif provider == "custom":
        display_name = questionary.text(t("Enter Display Name:"), default="Custom AI").ask()

        # Telemetry Note
        console.print(f"[green]{t('Note: Custom/BYOK models do not require telemetry enabled.')}[/green]")

        # Custom needs more details
        mode_data["ai:provider"] = "custom"

        # API Type
        api_type = questionary.select(
            t("Select API Type:"),
            choices=[
                "openai-chat",
                "openai-responses",
                "google-gemini"
            ],
            default="openai-chat"
        ).ask()
        mode_data["ai:apitype"] = api_type

        # Model
        model = questionary.text(t("Enter Model Name:"), default="llama3.3").ask()
        mode_data["ai:model"] = model

        # Endpoint
        endpoint = questionary.text(t("Enter Endpoint URL (e.g. http://localhost:11434/v1/chat/completions):"),
                                    default="http://localhost:11434/v1/chat/completions").ask()
        mode_data["ai:endpoint"] = endpoint

        # Token
        use_secret = questionary.confirm(t("Do you want to use a secret for the API Token?")).ask()
        if use_secret:
             secret_name = questionary.text(t("Enter Secret Name:")).ask()
             mode_data["ai:apitokensecretname"] = secret_name
             # Prompt to set secret
             console.print(f"[bold cyan]{t('Remember to run: wsh secret set {secret_name}=<your-key>')}[/bold cyan]")
        else:
             token = questionary.text(t("Enter API Token (or 'not-needed'/'ollama'):"), default="not-needed").ask()
             mode_data["ai:apitoken"] = token

        # Capabilities
        mode_data["ai:capabilities"] = _ask_capabilities()

    # 3. General Settings
    mode_data["display:name"] = display_name

    # Icon
    icon = questionary.text(t("Enter Icon Name (FontAwesome, e.g. robot, sparkles, brain) [optional]:"), default="").ask()
    if icon:
        mode_data["display:icon"] = icon

    # Thinking Level
    thinking = questionary.select(
        t("Select Thinking Level (optional):"),
        choices=[
            questionary.Choice(title=t("None"), value="none"),
            questionary.Choice(title=t("Quick (Low)"), value="low"),
            questionary.Choice(title=t("Balanced (Medium)"), value="medium"),
            questionary.Choice(title=t("Deep (High)"), value="high")
        ],
        default="none"
    ).ask()
    if thinking != "none":
        mode_data["ai:thinkinglevel"] = thinking

    # Generate Key
    # Sanitize display name for key
    sanitized = re.sub(r'[^a-zA-Z0-9]', '-', display_name.lower())
    sanitized = re.sub(r'-+', '-', sanitized).strip('-')
    default_key = sanitized

    key = questionary.text(t("Enter a unique ID for this mode (key in json):"), default=default_key).ask()

    # 4. Save
    cm = ConfigManager()
    cm.update_waveai_mode(key, mode_data)

    console.print(f"[green]{t('Successfully saved AI mode \'{display_name}\' to waveai.json')}[/green]")

    # 5. Set as Default
    set_default = questionary.confirm(t("Do you want to set this as your default AI mode?")).ask()
    if set_default:
        cm.set_config_value("waveai:defaultmode", key)
        console.print(f"[green]{t('Set \'{key}\' as the default AI mode.')}[/green]")

def _ask_capabilities():
    """Helper to ask for capabilities."""
    choices = [
        questionary.Choice("Tools (Read/Write files, run commands)", value="tools", checked=True),
        questionary.Choice("Images (Vision)", value="images"),
        questionary.Choice("PDFs (Read PDF content)", value="pdfs"),
        questionary.Choice("Listing (Directory Listing)", value="listing")
    ]

    caps = questionary.checkbox(
        t("Select Capabilities supported by this model:"),
        choices=choices
    ).ask()

    return caps
