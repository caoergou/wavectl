import pytest
from unittest.mock import patch, MagicMock
from wavectl.ai import configure_global_ai_settings

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
def test_configure_global_ai_settings_default_mode(mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {
        "mode1": {"display:name": "Mode 1"},
        "mode2": {"display:name": "Mode 2"}
    }
    mock_cm.load_settings.return_value = {
        "waveai:defaultmode": "mode1",
        "waveai:showcloudmodes": True
    }

    # User interactions:
    # 1. Main Menu -> Select "Default AI Mode" (value="defaultmode")
    # 2. Sub Menu -> Select "Mode 2" (value="mode2")
    # 3. Main Menu -> Select "Go Back" (value="back")
    mock_select.return_value.ask.side_effect = ["defaultmode", "mode2", "back"]

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:defaultmode", "mode2")

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
def test_configure_global_ai_settings_show_cloud(mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {
        "mode1": {"display:name": "Mode 1"}
    }
    mock_cm.load_settings.return_value = {
        "waveai:defaultmode": "mode1",
        "waveai:showcloudmodes": True
    }

    # User interactions:
    # 1. Main Menu -> Select "Show Cloud Modes" (value="showcloud")
    # 2. Sub Menu -> Select "Hide Cloud Modes" (value=False)
    # 3. Main Menu -> Select "Go Back" (value="back")
    mock_select.return_value.ask.side_effect = ["showcloud", False, "back"]

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:showcloudmodes", False)


@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_proxy(mock_text, mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {}
    mock_cm.load_waveai.return_value = {}

    # User interactions:
    # 1. Main Menu -> Select "AI Proxy URL" (value="proxy")
    # 2. Text Input -> Enter "http://proxy.com"
    # 3. Main Menu -> Select "Go Back" (value="back")
    mock_select.return_value.ask.side_effect = ["proxy", "back"]
    mock_text.return_value.ask.return_value = "http://proxy.com"

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("ai:proxyurl", "http://proxy.com")

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_fontsize(mock_text, mock_select, MockConfigManager):
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {}
    mock_cm.load_waveai.return_value = {}

    # 1. Select fontsize -> Enter "14"
    # 2. Back
    mock_select.return_value.ask.side_effect = ["fontsize", "back"]
    mock_text.return_value.ask.return_value = "14"

    configure_global_ai_settings()

    mock_cm.set_config_value.assert_called_with("ai:fontsize", 14)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_fixedfontsize(mock_text, mock_select, MockConfigManager):
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {}
    mock_cm.load_waveai.return_value = {}

    # 1. Select fixedfontsize -> Enter "12"
    # 2. Back
    mock_select.return_value.ask.side_effect = ["fixedfontsize", "back"]
    mock_text.return_value.ask.return_value = "12"

    configure_global_ai_settings()

    mock_cm.set_config_value.assert_called_with("ai:fixedfontsize", 12)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_fontsize_remove(mock_text, mock_select, MockConfigManager):
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {"ai:fontsize": 14}
    mock_cm.load_waveai.return_value = {}

    # 1. Select fontsize -> Enter "0" (to remove)
    # 2. Back
    mock_select.return_value.ask.side_effect = ["fontsize", "back"]
    mock_text.return_value.ask.return_value = "0"

    configure_global_ai_settings()

    mock_cm.set_config_value.assert_called_with("ai:fontsize", None)
