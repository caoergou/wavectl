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
    assert not (config_dir / "presets").exists() # Should not create presets anymore

def test_save_and_load_waveai(tmp_path):
    config_dir = tmp_path / "waveterm"
    cm = ConfigManager(config_dir=str(config_dir))

    mode_key = "openai-gpt4o"
    mode_data = {"display:name": "GPT-4o", "ai:provider": "openai"}

    cm.update_waveai_mode(mode_key, mode_data)

    loaded = cm.load_waveai()
    assert loaded[mode_key] == mode_data
    assert (config_dir / "waveai.json").exists()

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
def test_configure_ai_settings_openai(mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager, tmp_path):
    # Setup mocks for user input
    # Flow: Select Provider -> OpenAI -> Display Name -> Model -> Order -> Confirm Default

    # 1. Select Provider
    mock_select.return_value.ask.return_value = "OpenAI"

    # 2. Details
    # Display Name, Model, Order
    mock_text.return_value.ask.side_effect = ["My GPT", "gpt-4o", "1"]

    # 3. Confirm default
    mock_confirm.return_value.ask.return_value = True

    # Setup ConfigManager mock instance
    mock_cm_instance = MockConfigManager.return_value

    # Run the function
    configure_ai_settings()

    # Verify ConfigManager interactions
    # 1. update_waveai_mode should be called
    mock_cm_instance.update_waveai_mode.assert_called_once()
    args, _ = mock_cm_instance.update_waveai_mode.call_args
    key, data = args

    assert key == "openai-gpt-4o"
    assert data["display:name"] == "My GPT"
    assert data["ai:provider"] == "openai"
    assert data["ai:model"] == "gpt-4o"
    assert data["display:order"] == 1

    # 2. set_config_value should be called (since we said yes to default)
    mock_cm_instance.set_config_value.assert_called_with("waveai:defaultmode", key)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
def test_configure_ai_settings_ollama(mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager, tmp_path):
    # Flow: Select Provider -> Ollama -> Display Name -> Model -> Order -> Confirm Default

    mock_select.return_value.ask.return_value = "Ollama (Local)"
    mock_text.return_value.ask.side_effect = ["My Ollama", "llama3:latest", "2"]
    mock_confirm.return_value.ask.return_value = False

    mock_cm_instance = MockConfigManager.return_value

    configure_ai_settings()

    mock_cm_instance.update_waveai_mode.assert_called_once()
    args, _ = mock_cm_instance.update_waveai_mode.call_args
    key, data = args

    assert key == "ollama-llama3-latest"
    assert data["ai:apitype"] == "openai-chat"
    assert data["ai:endpoint"] == "http://localhost:11434/v1/chat/completions"
    assert data["ai:apitoken"] == "ollama"

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
def test_configure_ai_settings_openrouter(mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager, tmp_path):
    # Flow: Select Provider -> OpenRouter -> Display Name -> Model -> Capabilities -> Order -> Confirm Default

    mock_select.return_value.ask.return_value = "OpenRouter"
    mock_text.return_value.ask.side_effect = ["My OpenRouter", "vendor/model-v1", "3"]
    mock_checkbox.return_value.ask.return_value = ["tools", "images"] # Capabilities
    mock_confirm.return_value.ask.return_value = True

    mock_cm_instance = MockConfigManager.return_value

    configure_ai_settings()

    mock_cm_instance.update_waveai_mode.assert_called_once()
    args, _ = mock_cm_instance.update_waveai_mode.call_args
    key, data = args

    assert key == "openrouter-model-v1"
    assert data["ai:provider"] == "openrouter"
    assert data["ai:capabilities"] == ["tools", "images"]

    mock_cm_instance.set_config_value.assert_called_with("waveai:defaultmode", key)
