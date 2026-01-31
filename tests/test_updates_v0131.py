import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from wavectl.settings import configure_general_settings

class TestUpdatesV0131(unittest.TestCase):
    @patch("wavectl.settings.questionary")
    @patch("wavectl.settings.ConfigManager")
    @patch("wavectl.settings.console")
    def test_transparency_setting(self, mock_console, MockConfigManager, mock_questionary):
        # Setup mock config
        mock_cm = MockConfigManager.return_value
        mock_cm.load_settings.return_value = {"term:transparency": 1.0}

        # User flow: Select "transparency", enter "0.5", then "back"
        mock_questionary.select.return_value.ask.side_effect = ["transparency", "back"]
        mock_questionary.text.return_value.ask.return_value = "0.5"

        configure_general_settings()

        # Verify correct set_config_value call
        mock_cm.set_config_value.assert_called_with("term:transparency", 0.5)

    @patch("wavectl.settings.questionary")
    @patch("wavectl.settings.ConfigManager")
    @patch("wavectl.settings.console")
    def test_transparency_invalid(self, mock_console, MockConfigManager, mock_questionary):
        # Setup mock config
        mock_cm = MockConfigManager.return_value
        mock_cm.load_settings.return_value = {}

        # User flow: Select "transparency", enter "2.0" (invalid), then "back"
        mock_questionary.select.return_value.ask.side_effect = ["transparency", "back"]
        mock_questionary.text.return_value.ask.return_value = "2.0"

        configure_general_settings()

        # Verify set_config_value NOT called for transparency with invalid value
        call_args_list = mock_cm.set_config_value.call_args_list
        for call in call_args_list:
            if call[0][0] == "term:transparency":
                self.assertNotEqual(call[0][1], 2.0)

        # Check for error message
        found_error = False
        for call in mock_console.print.call_args_list:
            if call.args and "Value must be between" in str(call.args[0]):
                found_error = True
                break
        self.assertTrue(found_error, "Error message should be displayed for invalid input")

    @patch("wavectl.settings.questionary")
    @patch("wavectl.settings.ConfigManager")
    @patch("wavectl.settings.console")
    def test_bracketed_paste_setting(self, mock_console, MockConfigManager, mock_questionary):
        # Setup mock config
        mock_cm = MockConfigManager.return_value
        mock_cm.load_settings.return_value = {}

        # User flow: Select "allowbracketedpaste", confirm "True", then "back"
        mock_questionary.select.return_value.ask.side_effect = ["allowbracketedpaste", "back"]
        mock_questionary.confirm.return_value.ask.return_value = True

        configure_general_settings()

        # Verify correct set_config_value call
        mock_cm.set_config_value.assert_called_with("term:allowbracketedpaste", True)

if __name__ == "__main__":
    unittest.main()
