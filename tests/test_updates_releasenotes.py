from unittest.mock import patch, ANY
from wavectl.ai import configure_global_ai_settings
from wavectl.settings import configure_general_settings
from wavectl.i18n import t

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_settings_new_options(mock_text, mock_select, MockConfigManager):
    """Test configuring new global AI settings: proxyurl, fontsize, fixedfontsize."""

    mock_cm_instance = MockConfigManager.return_value
    # Mock initial settings to be empty/default
    mock_cm_instance.load_settings.return_value = {}
    mock_cm_instance.load_waveai.return_value = {}

    # Sequence of interactions:
    # 1. Select "proxyurl"
    # 2. Enter "http://proxy:8080"
    # 3. Select "fontsize"
    # 4. Enter "14"
    # 5. Select "fixedfontsize"
    # 6. Enter "12"
    # 7. Select "back"

    mock_select.return_value.ask.side_effect = [
        "proxyurl",
        "fontsize",
        "fixedfontsize",
        "back"
    ]

    mock_text.return_value.ask.side_effect = [
        "http://proxy:8080",
        "14",
        "12"
    ]

    configure_global_ai_settings()

    # Check calls
    mock_cm_instance.set_config_value.assert_any_call("ai:proxyurl", "http://proxy:8080")
    mock_cm_instance.set_config_value.assert_any_call("ai:fontsize", 14)
    mock_cm_instance.set_config_value.assert_any_call("ai:fixedfontsize", 12)


@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.confirm')
def test_configure_general_settings_hardware_accel(mock_confirm, mock_select, MockConfigManager):
    """Test configuring disablehardwareacceleration setting."""

    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_settings.return_value = {}

    # Flow: Select "disablehardwareacceleration" -> Confirm True -> Select "back"
    mock_select.return_value.ask.side_effect = ["disablehardwareacceleration", "back"]
    mock_confirm.return_value.ask.return_value = True

    configure_general_settings()

    mock_cm_instance.set_config_value.assert_called_with("window:disablehardwareacceleration", True)
