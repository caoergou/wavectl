import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from wavectl.settings import configure_general_settings
from wavectl.ai import add_ai_mode
from wavectl.config_manager import ConfigManager

# Add tests directory to path to import schema_validators
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schema_validators import ConfigValidator

@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.text')
@patch('wavectl.settings.console')
def test_new_terminal_settings(mock_console, mock_text, mock_select, MockConfigManager):
    """
    Test term:fontsize and term:fontfamily settings.
    """
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {}

    # Flow:
    # 1. Select termfontsize
    # 2. Enter "14"
    # 3. Select termfontfamily
    # 4. Enter "Fira Code"
    # 5. Back

    mock_select.return_value.ask.side_effect = [
        "termfontsize",
        "termfontfamily",
        "back"
    ]

    mock_text.return_value.ask.side_effect = [
        "14",
        "Fira Code"
    ]

    configure_general_settings()

    # Verify calls
    mock_cm.set_config_value.assert_any_call("term:fontsize", 14)
    mock_cm.set_config_value.assert_any_call("term:fontfamily", "Fira Code")

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
@patch('wavectl.ai.console')
def test_add_ai_mode_openai_defaults(mock_console, mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager):
    """
    Test OpenAI default model (gpt-5.1) and max tokens prompt.
    """
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {}

    # Flow for OpenAI:
    # 1. Select "openai"
    # 2. Display Name (default check)
    # 3. Model (default check)
    # 4. Secret confirm (Yes)
    # 5. Icon (skip)
    # 6. Thinking Level (None)
    # 7. Max Tokens ("2000")
    # 8. Key ("openai-gpt-5-1")
    # 9. Set Default (No)

    mock_select.return_value.ask.side_effect = [
        "openai", # Provider
        "none",   # Thinking
    ]

    # We need to capture the default values passed to text prompts to verify them
    # But side_effect just returns values. We can inspect call_args later.

    mock_text.return_value.ask.side_effect = [
        "OpenAI GPT-5.1", # Display Name
        "gpt-5.1",        # Model
        "",               # Icon
        "2000",           # Max Tokens
        "openai-gpt-5-1"  # Key
    ]

    mock_confirm.return_value.ask.side_effect = [
        True, # Has Secret
        False # Set Default
    ]

    add_ai_mode()

    # Verify defaults were correct in the prompts
    # 1. Display Name prompt
    call_args_display = mock_text.call_args_list[0]
    assert call_args_display[1]['default'] == "OpenAI GPT-5.1"

    # 2. Model Name prompt
    call_args_model = mock_text.call_args_list[1]
    assert call_args_model[1]['default'] == "gpt-5.1"

    # Verify update_waveai_mode called with correct data including maxtokens
    expected_data = {
        "ai:provider": "openai",
        "ai:model": "gpt-5.1",
        "display:name": "OpenAI GPT-5.1",
        "ai:maxtokens": 2000
    }
    mock_cm.update_waveai_mode.assert_called_with("openai-gpt-5-1", expected_data)

@patch('wavectl.ai.ConfigManager')
@patch('wavectl.ai.questionary.select')
@patch('wavectl.ai.questionary.text')
@patch('wavectl.ai.questionary.confirm')
@patch('wavectl.ai.questionary.checkbox')
@patch('wavectl.ai.console')
def test_add_ai_mode_openrouter_defaults(mock_console, mock_checkbox, mock_confirm, mock_text, mock_select, MockConfigManager):
    """
    Test OpenRouter default model (claude-3.5-sonnet).
    """
    mock_cm = MockConfigManager.return_value
    mock_cm.load_waveai.return_value = {}

    # Flow for OpenRouter:
    # 1. Select "openrouter"
    # 2. Display Name
    # 3. Model
    # 4. Secret confirm (Yes)
    # 5. Capabilities
    # 6. Icon
    # 7. Thinking Level
    # 8. Max Tokens
    # 9. Key
    # 10. Set Default

    mock_select.return_value.ask.side_effect = [
        "openrouter",
        "none" # Thinking
    ]

    mock_text.return_value.ask.side_effect = [
        "OpenRouter",
        "anthropic/claude-3.5-sonnet",
        "", # Icon
        "", # Max Tokens (skip)
        "openrouter" # Key
    ]

    mock_confirm.return_value.ask.side_effect = [
        True, # Secret
        False # Default
    ]

    mock_checkbox.return_value.ask.return_value = ["tools"]

    add_ai_mode()

    # Verify defaults
    call_args_model = mock_text.call_args_list[1]
    assert call_args_model[1]['default'] == "anthropic/claude-3.5-sonnet"

    # Verify data
    expected_data = {
        "ai:provider": "openrouter",
        "ai:model": "anthropic/claude-3.5-sonnet",
        "display:name": "OpenRouter",
        "ai:capabilities": ["tools"]
    }
    # Note: ai:maxtokens should NOT be present if skipped
    mock_cm.update_waveai_mode.assert_called_with("openrouter", expected_data)
