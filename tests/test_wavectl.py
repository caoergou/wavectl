import json
import os
import shutil
from pathlib import Path
from wavectl.config_manager import ConfigManager
from wavectl.ai import configure_ai_settings
from unittest.mock import patch

def test_config_manager_creation(tmp_path):
    # Setup mock config dir
    config_dir = tmp_path / "waveterm"
    cm = ConfigManager(config_dir=str(config_dir))

    assert cm.config_dir.exists()
    assert cm.presets_dir.exists()
    assert (config_dir / "presets").exists()

def test_save_and_load_settings(tmp_path):
    config_dir = tmp_path / "waveterm"
    cm = ConfigManager(config_dir=str(config_dir))

    settings = {"theme": "dark"}
    cm.save_settings(settings)

    loaded = cm.load_settings()
    assert loaded == settings
    assert (config_dir / "settings.json").exists()

def test_update_preset(tmp_path):
    config_dir = tmp_path / "waveterm"
    cm = ConfigManager(config_dir=str(config_dir))

    preset_key = "ai@test"
    preset_data = {"display:name": "Test Preset"}

    cm.update_preset("ai.json", preset_key, preset_data)

    presets = cm.load_presets("ai.json")
    assert presets[preset_key] == preset_data
    assert (config_dir / "presets" / "ai.json").exists()

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.password')
@patch('wavectl.ai.questionary.confirm')
def test_configure_ai_settings_openai(mock_confirm, mock_password, mock_text, mock_select, MockConfigManager, tmp_path):
    # Setup mocks for user input
    # Flow: Select Provider -> OpenAI -> Model -> Key -> Preset Name -> Confirm Default

    # 1. Select Provider
    mock_select.return_value.ask.return_value = "OpenAI"

    # 2. Details
    mock_text.return_value.ask.side_effect = ["gpt-4o", "My OpenAI"] # Model, Preset Name
    mock_password.return_value.ask.return_value = "sk-test-key"

    # 3. Confirm default
    mock_confirm.return_value.ask.return_value = True

    # Setup ConfigManager mock instance
    mock_cm_instance = MockConfigManager.return_value

    # Run the function
    configure_ai_settings()

    # Verify ConfigManager interactions
    # 1. update_preset should be called
    mock_cm_instance.update_preset.assert_called_once()
    args, _ = mock_cm_instance.update_preset.call_args
    filename, key, data = args

    assert filename == "ai.json"
    assert "ai@openai-gpt-4o" in key # basic check on key generation logic
    assert data["ai:apitype"] == "openai"
    assert data["ai:model"] == "gpt-4o"
    assert data["ai:apitoken"] == "sk-test-key"

    # 2. set_config_value should be called (since we said yes to default)
    mock_cm_instance.set_config_value.assert_called_with("ai:preset", key)
