from unittest.mock import patch
from wavectl.ssh import configure_ssh_connections
from wavectl.theme import configure_theme
from wavectl.widgets import configure_widgets

@patch('wavectl.ssh.ConfigManager')
@patch('wavectl.ssh.questionary.select')
@patch('wavectl.ssh.questionary.text')
@patch('wavectl.ssh.questionary.confirm')
@patch('wavectl.ssh.questionary.path')
def test_configure_ssh_connections(mock_path, mock_confirm, mock_text, mock_select, MockConfigManager):
    # Flow: Select Action -> Add New -> Details -> Confirm Key -> Path -> Save
    mock_select.return_value.ask.side_effect = ["Add New SSH Connection", "Go Back"]
    mock_text.return_value.ask.side_effect = ["My Server", "192.168.1.1", "user", "2222"]
    mock_confirm.return_value.ask.return_value = True
    mock_path.return_value.ask.return_value = "/path/to/key"

    mock_cm_instance = MockConfigManager.return_value

    configure_ssh_connections()

    # Verify ConfigManager update_preset call
    mock_cm_instance.update_preset.assert_called_once()
    args, _ = mock_cm_instance.update_preset.call_args
    filename, key, data = args

    assert filename == "term.json"
    assert "term@ssh-my-server" in key
    assert "ssh -p 2222 -i /path/to/key user@192.168.1.1" in data["term:cmd"]


@patch('wavectl.theme.ConfigManager')
@patch('wavectl.theme.questionary.select')
def test_configure_theme(mock_select, MockConfigManager):
    mock_select.return_value.ask.return_value = "Dracula"

    mock_cm_instance = MockConfigManager.return_value

    configure_theme()

    mock_cm_instance.set_config_value.assert_called_with("theme", "dracula")

@patch('wavectl.widgets.ConfigManager')
@patch('wavectl.widgets.questionary.checkbox')
def test_configure_widgets(mock_checkbox, MockConfigManager):
    mock_checkbox.return_value.ask.return_value = ["CPU Usage", "Weather"]

    mock_cm_instance = MockConfigManager.return_value

    configure_widgets()

    mock_cm_instance.set_config_value.assert_called_with("widgets", ["CPU Usage", "Weather"])
