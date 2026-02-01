import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from wavectl.settings import configure_general_settings
from wavectl.config_manager import ConfigManager

# Add tests directory to path to import schema_validators
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schema_validators import ConfigValidator

@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.text')
@patch('wavectl.settings.questionary.confirm')
@patch('wavectl.settings.console')
def test_configure_general_settings_v0131(mock_console, mock_confirm, mock_text, mock_select, MockConfigManager):
    """
    Test the new configuration options added for v0.13.1 updates.
    """

    # Setup Mock ConfigManager
    mock_cm = MockConfigManager.return_value
    # Initial settings
    mock_cm.load_settings.return_value = {}

    # Sequence of user interactions:
    # 1. Select "transparency" -> Enter "0.5"
    # 2. Select "disablehardwareacceleration" -> Confirm True
    # 3. Select "allowbracketedpaste" -> Confirm False
    # 4. Select "editorwordwrap" -> Confirm True
    # 5. Select "webhomedefault" -> Enter "https://example.com"
    # 6. Select "back" to exit

    mock_select.return_value.ask.side_effect = [
        "transparency",
        "disablehardwareacceleration",
        "allowbracketedpaste",
        "editorwordwrap",
        "webhomedefault",
        "back"
    ]

    # Text inputs for transparency and webhomedefault
    # transparency: "0.5"
    # webhomedefault: "https://example.com"
    mock_text.return_value.ask.side_effect = [
        "0.5",
        "https://example.com"
    ]

    # Confirm inputs
    # disablehardwareacceleration: True
    # allowbracketedpaste: False
    # editorwordwrap: True
    mock_confirm.return_value.ask.side_effect = [
        True,
        False,
        True
    ]

    # Run the function
    configure_general_settings()

    # Verify calls to set_config_value
    # We expect 5 calls with specific values

    calls = mock_cm.set_config_value.call_args_list
    assert len(calls) == 5

    # Check each expected call
    # 1. transparency
    mock_cm.set_config_value.assert_any_call("term:transparency", 0.5)

    # 2. disablehardwareacceleration
    mock_cm.set_config_value.assert_any_call("window:disablehardwareacceleration", True)

    # 3. allowbracketedpaste
    mock_cm.set_config_value.assert_any_call("term:allowbracketedpaste", False)

    # 4. editorwordwrap
    mock_cm.set_config_value.assert_any_call("editor:wordwrap", True)

    # 5. webhomedefault
    mock_cm.set_config_value.assert_any_call("web:homedefault", "https://example.com")

    # Verify Schema Validation for the generated settings
    # Construct a dictionary simulating the result
    simulated_settings = {
        "term:transparency": 0.5,
        "window:disablehardwareacceleration": True,
        "term:allowbracketedpaste": False,
        "editor:wordwrap": True,
        "web:homedefault": "https://example.com"
    }

    # This should not raise an error
    ConfigValidator.validate("settings.json", simulated_settings)

@patch('wavectl.settings.ConfigManager')
@patch('wavectl.settings.questionary.select')
@patch('wavectl.settings.questionary.text')
@patch('wavectl.settings.console')
def test_transparency_validation(mock_console, mock_text, mock_select, MockConfigManager):
    """
    Test validation for transparency (float 0.0-1.0).
    """
    mock_cm = MockConfigManager.return_value
    mock_cm.load_settings.return_value = {}

    # Flow:
    # 1. Select transparency
    # 2. Enter invalid "abc" (should print error)
    # 3. Select transparency
    # 4. Enter invalid "1.5" (should print error)
    # 5. Select transparency
    # 6. Enter valid "0.8"
    # 7. Back

    mock_select.return_value.ask.side_effect = [
        "transparency",
        "transparency",
        "transparency",
        "back"
    ]

    mock_text.return_value.ask.side_effect = [
        "abc",
        "1.5",
        "0.8"
    ]

    configure_general_settings()

    # Verify set_config_value was called only once with 0.8
    mock_cm.set_config_value.assert_called_once_with("term:transparency", 0.8)
