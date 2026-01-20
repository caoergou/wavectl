import json
import os
import shutil
from pathlib import Path
from wavectl.config_manager import ConfigManager
from wavectl.ai import add_ai_mode
from unittest.mock import patch
from tests.schema_validators import ConfigValidator

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

    settings = {
        "term:theme": "dark",
        "term:macoptionismeta": True
    }
    cm.save_settings(settings)

    loaded = cm.load_settings()
    assert loaded == settings
    assert (config_dir / "settings.json").exists()

    # Validate
    ConfigValidator.validate("settings.json", loaded)

def test_update_preset(tmp_path):
    config_dir = tmp_path / "waveterm"
    cm = ConfigManager(config_dir=str(config_dir))

    # Using a valid bg preset for test since ai presets are deprecated/different structure
    preset_key = "bg@test"
    preset_data = {"display:name": "Test Preset", "bg": "red"}

    cm.update_preset("presets.json", preset_key, preset_data)

    presets = cm.load_presets("presets.json")
    assert presets[preset_key] == preset_data
    assert (config_dir / "presets" / "presets.json").exists()

    # Validate
    ConfigValidator.validate("presets.json", presets)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.password')
@patch('wavectl.ai.questionary.confirm')
def test_add_ai_mode_openai(mock_confirm, mock_password, mock_text, mock_select, MockConfigManager, tmp_path):
    # This test verifies the LOGIC of add_ai_mode, but we also want to verify the SCHEMA it produces.
    # Since it uses a MockConfigManager, it doesn't write to disk. We intercept the call.

    # Setup mocks for user input
    # Flow:
    # 1. Select Provider -> "openai"
    # 2. Display Name -> "My OpenAI"
    # 3. Model -> "gpt-5.1"
    # 4. Secret Confirm -> False
    # 5. Secret Input -> "sk-test-key"
    # 6. Icon -> "brain"
    # 7. Thinking -> "medium" (value)
    # 8. Key -> "my-openai"
    # 9. Confirm Default -> True

    # 1. Select Provider & Thinking
    mock_select.return_value.ask.side_effect = ["openai", "medium"]

    # 2. Text Inputs
    mock_text.return_value.ask.side_effect = [
        "My OpenAI", # Display Name
        "gpt-5.1",   # Model
        "brain",     # Icon
        "my-openai"  # Key
    ]

    # 3. Passwords
    mock_password.return_value.ask.return_value = "sk-test-key"

    # 4. Confirmations
    mock_confirm.return_value.ask.side_effect = [False, True] # Secret present? No. Set Default? Yes.

    # Setup ConfigManager mock instance
    mock_cm_instance = MockConfigManager.return_value

    # Run the function
    add_ai_mode()

    # Verify ConfigManager interactions
    # 1. update_waveai_mode should be called
    mock_cm_instance.update_waveai_mode.assert_called_once()
    args, _ = mock_cm_instance.update_waveai_mode.call_args
    key, data = args

    # Verify the keys are modern
    assert key == "my-openai"

    # Check data content
    assert data["ai:provider"] == "openai"
    assert data["ai:model"] == "gpt-5.1"
    assert data["display:icon"] == "brain"
    assert data["ai:thinkinglevel"] == "medium"
    # Note: Secret is not stored in waveai.json for openai, it's just set via wsh secret set command printed to user.
    # But for 'custom' it might be different. OpenAI uses standard env var or secret key.
    # verify logic:
    # if provider == "openai": ...
    # console.print ... wsh secret set ...
    # mode_data["ai:provider"] = "openai"
    # mode_data["ai:model"] = model

    # Validate against schema
    simulation_waveai = {key: data}
    ConfigValidator.validate("waveai.json", simulation_waveai)

    # 2. set_config_value should be called (since we said yes to default)
    mock_cm_instance.set_config_value.assert_called_with("waveai:defaultmode", key)
