from unittest.mock import patch, ANY
from wavectl.ai import add_ai_mode
from wavectl.settings import configure_general_settings
from wavectl.i18n import t

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
def test_add_ai_mode_maxtokens(mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test adding an AI mode with max tokens."""

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
    assert data["ai:maxtokens"] == 4096


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.text')
@patch('wavectl.settings.questionary.confirm')
def test_configure_transparency(mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test configuring term:transparency setting."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Flow: Select "transparency" -> Enter "0.8" -> Select "back"
    mock_select.return_value.ask.side_effect = ["transparency", "back"]
    mock_text.return_value.ask.return_value = "0.8"

    configure_general_settings()

    mock_cm_instance.set_config_value.assert_called_with("term:transparency", 0.8)


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.confirm')
def test_configure_disablehardwareacceleration(mock_confirm, mock_select, MockConfigManager):
    """Test configuring window:disablehardwareacceleration setting."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Flow: Select "disablehardwareacceleration" -> Confirm True -> Select "back"
    mock_select.return_value.ask.side_effect = ["disablehardwareacceleration", "back"]
    mock_confirm.return_value.ask.return_value = True

    configure_general_settings()

    mock_cm_instance.set_config_value.assert_called_with("window:disablehardwareacceleration", True)


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.confirm')
def test_configure_allowbracketedpaste(mock_confirm, mock_select, MockConfigManager):
    """Test configuring term:allowbracketedpaste setting."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Flow: Select "allowbracketedpaste" -> Confirm False -> Select "back"
    mock_select.return_value.ask.side_effect = ["allowbracketedpaste", "back"]
    mock_confirm.return_value.ask.return_value = False

    configure_general_settings()

    mock_cm_instance.set_config_value.assert_called_with("term:allowbracketedpaste", False)
