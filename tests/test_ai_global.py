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
    # 1. Select Setting -> "defaultmode"
    # 2. Select Default Mode -> "mode2"
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["defaultmode", "mode2", "back"]

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:defaultmode", "mode2")
    assert mock_cm.set_config_value.call_count == 1

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.confirm')
def test_configure_global_ai_settings_show_cloud(mock_confirm, mock_select, MockConfigManager):
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
    # 1. Select Setting -> "showcloudmodes"
    # 2. Confirm -> False (handled by mock_confirm)
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["showcloudmodes", "back"]
    mock_confirm.return_value.ask.return_value = False

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:showcloudmodes", False)
    assert mock_cm.set_config_value.call_count == 1

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_settings_proxy(mock_text, mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {}
    mock_cm.load_settings.return_value = {}

    # User interactions:
    # 1. Select Setting -> "proxyurl"
    # 2. Enter URL -> "http://proxy.com"
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["proxyurl", "back"]
    mock_text.return_value.ask.return_value = "http://proxy.com"

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("ai:proxyurl", "http://proxy.com")

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_settings_fontsize(mock_text, mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {}
    mock_cm.load_settings.return_value = {}

    # User interactions:
    # 1. Select Setting -> "fontsize"
    # 2. Enter Size -> "16"
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["fontsize", "back"]
    mock_text.return_value.ask.return_value = "16"

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("ai:fontsize", 16)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
def test_configure_global_ai_settings_fixedfontsize(mock_text, mock_select, MockConfigManager):
    # Setup mocks
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {}
    mock_cm.load_settings.return_value = {}

    # User interactions:
    # 1. Select Setting -> "fixedfontsize"
    # 2. Enter Size -> "14"
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["fixedfontsize", "back"]
    mock_text.return_value.ask.return_value = "14"

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("ai:fixedfontsize", 14)
