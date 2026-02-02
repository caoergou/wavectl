import pytest
import sys
import os
from unittest.mock import patch
from wavectl.ssh import add_ssh_connection

# Add tests directory to path to import schema_validators
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schema_validators import ConfigValidator

@patch('wavectl.ssh.ConfigManager')
@patch('wavectl.ssh.questionary.select')
@patch('wavectl.ssh.questionary.text')
@patch('wavectl.ssh.questionary.confirm')
@patch('wavectl.ssh.questionary.path')
@patch('wavectl.ssh.console')
def test_add_ssh_connection_with_env(mock_console, mock_path, mock_confirm, mock_text, mock_select, MockConfigManager):
    """
    Test adding an SSH connection with environment variables.
    """

    # User Interaction Flow:
    # 1. Hostname -> "myserver"
    # 2. Username -> "user"
    # 3. Port -> "22"
    # 4. Identity File Confirm -> False
    # 5. Alias -> "MyServer"
    # 6. Password Secret Confirm -> False
    # 7. Configure Env -> True
    # 8. Env Name -> "MY_VAR"
    # 9. Env Value -> "my_val"
    # 10. Env Name -> "" (Finish)

    # Mock text inputs
    mock_text.return_value.ask.side_effect = [
        "myserver", # Hostname
        "user",     # Username
        "22",       # Port
        "MyServer", # Alias
        "MY_VAR",   # Env Name 1
        "my_val",   # Env Value 1
        ""          # Env Name 2 (Finish)
    ]

    # Mock confirm inputs
    # 1. Identity File -> False
    # 2. Password Secret -> False
    # 3. Configure Env -> True
    mock_confirm.return_value.ask.side_effect = [
        False,
        False,
        True
    ]

    # Setup ConfigManager
    mock_cm = MockConfigManager.return_value

    # Run
    add_ssh_connection()

    # Verify update_connection call
    mock_cm.update_connection.assert_called_once()
    key, data = mock_cm.update_connection.call_args[0]

    assert key == "MyServer"
    assert data["ssh:hostname"] == "myserver"
    assert data["ssh:user"] == "user"
    assert "cmd:env" in data
    assert data["cmd:env"] == {"MY_VAR": "my_val"}

    # Validate against schema
    # Wrap in connections structure
    simulation_connections = {key: data}
    ConfigValidator.validate("connections.json", simulation_connections)
