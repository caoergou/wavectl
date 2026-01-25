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
    # 2. Select Default AI Mode -> "mode2"
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["defaultmode", "mode2", "back"]

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:defaultmode", "mode2")
    assert mock_cm.set_config_value.call_count == 1

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
    # 1. Select Setting -> "showcloudmodes"
    # 2. Show Cloud Modes -> False
    # 3. Select Setting -> "back"
    mock_select.return_value.ask.side_effect = ["showcloudmodes", False, "back"]

    # Run
    configure_global_ai_settings()

    # Verify
    mock_cm.set_config_value.assert_called_with("waveai:showcloudmodes", False)
    assert mock_cm.set_config_value.call_count == 1
