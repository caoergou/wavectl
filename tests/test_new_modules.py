from unittest.mock import patch, MagicMock
from wavectl.ssh import configure_ssh_connections
from wavectl.theme import configure_theme
from wavectl.widgets import configure_widgets

@patch('wavectl.ssh.ConfigManager')
@patch('wavectl.ssh.questionary.select')
@patch('wavectl.ssh.questionary.text')
@patch('wavectl.ssh.questionary.confirm')
@patch('wavectl.ssh.questionary.path')
def test_configure_ssh_connections(mock_path, mock_confirm, mock_text, mock_select, MockConfigManager):
    # Flow: Select Action -> Add New -> Hostname -> User -> Port -> Key Confirm -> Key Path -> Alias -> Save
    mock_select.return_value.ask.side_effect = ["Add New SSH Connection", "Go Back"]
    # text asks: Hostname, Username, Port, Alias
    mock_text.return_value.ask.side_effect = ["192.168.1.1", "user", "2222", "Production DB"]
    mock_confirm.return_value.ask.return_value = True
    mock_path.return_value.ask.return_value = "/path/to/key"

    mock_cm_instance = MockConfigManager.return_value

    configure_ssh_connections()

    # Verify ConfigManager update_connection call
    mock_cm_instance.update_connection.assert_called_once()
    key, data = mock_cm_instance.update_connection.call_args[0]

    assert key == "Production DB"
    assert data["ssh:hostname"] == "192.168.1.1"
    assert data["ssh:user"] == "user"
    assert data["ssh:port"] == "2222"
    assert data["ssh:identityfile"] == ["/path/to/key"]


@patch('wavectl.theme.ConfigManager')
@patch('wavectl.theme.questionary.select')
def test_configure_theme(mock_select, MockConfigManager):
    mock_select.return_value.ask.return_value = "Dracula"

    mock_cm_instance = MockConfigManager.return_value

    configure_theme()

    mock_cm_instance.set_config_value.assert_called_with("term:theme", "dracula")

@patch('wavectl.widgets.ConfigManager')
@patch('wavectl.widgets.questionary.checkbox')
def test_configure_widgets(mock_checkbox, MockConfigManager):
    # Setup initial state: all defaults enabled (empty dict or no nulls)
    mock_cm_instance = MockConfigManager.return_value
    mock_cm_instance.load_widgets.return_value = {}

    # User unchecks "Terminal" (defwidget@terminal), keeps others
    # Expected: "defwidget@terminal" set to None (null)

    # checkbox returns list of SELECTED values
    # Let's say user selects Files and Web. Terminal is NOT selected.
    mock_checkbox.return_value.ask.return_value = ["defwidget@files", "defwidget@web", "defwidget@ai", "defwidget@sysinfo"]

    configure_widgets()

    # update_widget should be called for "defwidget@terminal" with None
    mock_cm_instance.update_widget.assert_called_with("defwidget@terminal", None)

    # And potentially remove_widget_override for others if they were previously disabled (but here they weren't)
