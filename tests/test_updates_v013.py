from unittest.mock import patch, ANY
from wavectl.ai import add_ai_mode
from wavectl.settings import configure_general_settings
from wavectl.i18n import t

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
def test_add_ai_mode_custom_llama(mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test adding a custom AI mode with default llama3.3 model."""

    mock_select.return_value.ask.side_effect = ["custom", "openai-chat", "none"]

    mock_text.return_value.ask.side_effect = [
        "Local Llama",  # Display Name
        "llama3.3",     # Model
        "http://localhost:11434/v1/chat/completions", # Endpoint
        "not-needed",   # Token
        "brain",        # Icon
        "4096",         # Max Tokens
        "local-llama"   # Key
    ]

    mock_confirm.return_value.ask.side_effect = [False, False]
    mock_checkbox.return_value.ask.return_value = ["tools"]

    mock_cm_instance = MockConfigManager.return_value

    add_ai_mode()

    # Verify ConfigManager update_waveai_mode call
    mock_cm_instance.update_waveai_mode.assert_called_once()
    key, data = mock_cm_instance.update_waveai_mode.call_args[0]

    assert key == "local-llama"
    assert data["ai:provider"] == "custom"
    assert data["ai:model"] == "llama3.3"
    assert data["ai:maxtokens"] == 4096

    # Verify defaults in calls
    mock_text.assert_any_call(t("Enter Model Name:"), default="llama3.3")


@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.password')
@patch('wavectl.ai.questionary.checkbox')
def test_add_ai_mode_defaults_openai(mock_checkbox, mock_password, mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test default values for OpenAI."""
    # Flow for OpenAI:
    # Select "openai"
    # Text "OpenAI GPT-5.1" (Display Name)
    # Text "gpt-5.1" (Model Name)
    # Confirm True (Has Secret)
    # Text "icon" (Icon)
    # Select "none" (Thinking)
    # Text "" (Max Tokens - default empty)
    # Text "openai-gpt-5-1" (Key)
    # Confirm False (Set as default)

    mock_select.return_value.ask.side_effect = ["openai", "none"]
    mock_text.return_value.ask.side_effect = [
        "OpenAI GPT-5.1",
        "gpt-5.1",
        "icon",
        "", # max tokens
        "openai-gpt-5-1"
    ]
    mock_confirm.return_value.ask.side_effect = [True, False]

    add_ai_mode()

    found_openai = False
    for call in mock_text.call_args_list:
        args, kwargs = call
        if args[0] == t("Enter Model Name:"):
            if kwargs.get("default") == "gpt-5.1":
                found_openai = True
    assert found_openai, "Default model for OpenAI should be gpt-5.1"


@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.password')
@patch('wavectl.ai.questionary.checkbox')
def test_add_ai_mode_defaults_openrouter(mock_checkbox, mock_password, mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test default values for OpenRouter."""
    # 2. Test OpenRouter Defaults
    mock_select.return_value.ask.side_effect = ["openrouter", "none"]
    mock_text.return_value.ask.side_effect = [
        "OpenRouter",
        "anthropic/claude-3.5-sonnet",
        "icon",
        "", # max tokens
        "openrouter"
    ]
    mock_confirm.return_value.ask.side_effect = [True, False]
    mock_checkbox.return_value.ask.return_value = ["tools"]

    add_ai_mode()

    found_or = False
    for call in mock_text.call_args_list:
        args, kwargs = call
        if args[0] == t("Enter Model Name (e.g. anthropic/claude-3.5-sonnet):"):
             if kwargs.get("default") == "anthropic/claude-3.5-sonnet":
                 found_or = True
    assert found_or, "Default model for OpenRouter should be anthropic/claude-3.5-sonnet"


@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.password')
@patch('wavectl.ai.questionary.checkbox')
def test_add_ai_mode_defaults_google(mock_checkbox, mock_password, mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test default values for Google."""
    # 3. Test Google Defaults
    mock_select.return_value.ask.side_effect = ["google", "none"]
    mock_text.return_value.ask.side_effect = [
        "Google Gemini",
        "gemini-1.5-pro",
        "icon",
        "", # max tokens
        "google-gemini"
    ]
    mock_confirm.return_value.ask.side_effect = [True, False]

    add_ai_mode()

    found_google = False
    for call in mock_text.call_args_list:
        args, kwargs = call
        if args[0] == t("Enter Model Name:"):
             if kwargs.get("default") == "gemini-1.5-pro":
                 found_google = True
    assert found_google, "Default model for Google should be gemini-1.5-pro"


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.confirm')
def test_configure_macoptionismeta(mock_confirm, mock_select, MockConfigManager):
    """Test configuring term:macoptionismeta setting."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Flow: Select "macoptionismeta" -> Confirm True -> Select "back"
    mock_select.return_value.ask.side_effect = ["macoptionismeta", "back"]
    mock_confirm.return_value.ask.return_value = True

    configure_general_settings()

    mock_cm_instance.set_config_value.assert_called_with("term:macoptionismeta", True)
