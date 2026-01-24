from unittest.mock import patch, ANY
from wavectl.settings import configure_general_settings
from wavectl.ai import configure_global_ai_settings
from wavectl.i18n import t

@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.text')
@patch('wavectl.settings.questionary.confirm')
def test_configure_term_settings(mock_confirm, mock_text, mock_select, MockConfigManager):
    """Test configuring terminal settings (fontsize, fontfamily, transparency)."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Sequence:
    # 1. term:fontsize -> "16" -> back
    # 2. term:fontfamily -> "Fira Code" -> back
    # 3. term:transparency -> "0.9" -> back

    # 1. Font Size
    mock_select.return_value.ask.side_effect = ["termfontsize", "back"]
    mock_text.return_value.ask.return_value = "16"
    configure_general_settings()
    mock_cm_instance.set_config_value.assert_called_with("term:fontsize", 16)

    # 2. Font Family
    mock_select.return_value.ask.side_effect = ["termfontfamily", "back"]
    mock_text.return_value.ask.return_value = "Fira Code"
    configure_general_settings()
    mock_cm_instance.set_config_value.assert_called_with("term:fontfamily", "Fira Code")

    # 3. Transparency
    mock_select.return_value.ask.side_effect = ["termtransparency", "back"]
    mock_text.return_value.ask.return_value = "0.9"
    configure_general_settings()
    mock_cm_instance.set_config_value.assert_called_with("term:transparency", 0.9)


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.confirm')
def test_configure_window_widget_settings(mock_confirm, mock_select, MockConfigManager):
    """Test configuring window and widget settings."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # 1. Disable Hardware Acceleration
    mock_select.return_value.ask.side_effect = ["disablehardwareacceleration", "back"]
    mock_confirm.return_value.ask.return_value = True
    configure_general_settings()
    mock_cm_instance.set_config_value.assert_called_with("window:disablehardwareacceleration", True)

    # 2. Show Help Widget
    mock_select.return_value.ask.side_effect = ["showhelp", "back"]
    mock_confirm.return_value.ask.return_value = False
    configure_general_settings()
    mock_cm_instance.set_config_value.assert_called_with("widget:showhelp", False)


@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_settings_new(mock_text, mock_confirm, mock_select, MockConfigManager):
    """Test configuring new global AI settings."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_waveai.return_value = {"default": {}} # Need some mode to avoid "No AI modes" exit
    mock_cm_instance.load_settings.return_value = {}

    # Flow:
    # 1. Select Default Mode -> Skip
    # 2. Show Cloud Modes -> Keep Current (Skip)
    # 3. Proxy URL -> Yes -> "http://proxy"
    # 4. Font Size -> Yes -> "18"
    # 5. Fixed Font Size -> Yes -> "16"

    # We need to set side_effects for the return values of .ask()

    # Select calls:
    # 1. Select Default AI Mode
    # 2. Show Built-in Cloud Modes
    mock_select.return_value.ask.side_effect = ["skip", "skip"]

    # Confirm calls:
    # 1. Configure Proxy?
    # 2. Configure Font Size?
    # 3. Configure Fixed Font Size?
    mock_confirm.return_value.ask.side_effect = [True, True, True]

    # Text calls:
    # 1. Enter Proxy URL
    # 2. Enter Font Size
    # 3. Enter Fixed Font Size
    mock_text.return_value.ask.side_effect = ["http://proxy", "18", "16"]

    configure_global_ai_settings()

    mock_cm_instance.set_config_value.assert_any_call("ai:proxyurl", "http://proxy")
    mock_cm_instance.set_config_value.assert_any_call("ai:fontsize", 18)
    mock_cm_instance.set_config_value.assert_any_call("ai:fixedfontsize", 16)
