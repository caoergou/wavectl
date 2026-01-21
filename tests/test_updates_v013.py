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

    # Verify defaults in calls
    # Use assert_any_call to find if the call was made with correct default
    # Note: t("Enter Model Name:") will return "Enter Model Name:" in en_US
    mock_text.assert_any_call(t("Enter Model Name:"), default="llama3.3")


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
