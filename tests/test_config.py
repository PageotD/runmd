import unittest
from unittest.mock import patch
from runmd.config import copy_config, load_config, validate_config, get_default_config_path, get_languages

class TestRunmdConfig(unittest.TestCase):

    @patch('pkg_resources.resource_filename')
    @patch('os.path.exists')
    @patch('shutil.copy')
    @patch('builtins.print')
    def test_copy_config_success(self, mock_print, mock_copy, mock_exists, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.return_value = "mock_source_path/config.json"
        mock_exists.side_effect = lambda path: path == "mock_dest_path"
        mock_copy.return_value = None

        with patch('os.path.expanduser', return_value="mock_dest_path/config.json"):
            copy_config()

        # Assert correct calls
        mock_resource_filename.assert_called_once_with("runmd", "config.json")
        mock_copy.assert_called_once_with("mock_source_path/config.json", "mock_dest_path/config.json")
        mock_print.assert_called_once_with("Configuration file copied to mock_dest_path/config.json.")

    @patch('pkg_resources.resource_filename')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.copy')
    @patch('builtins.print')
    def test_copy_config_already_exists(self, mock_print, mock_copy, mock_makedirs, mock_exists, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.return_value = "mock_source_path/config.json"
        mock_exists.side_effect = lambda path: True  # Simulate that destination exists

        with patch('os.path.expanduser', return_value="mock_dest_path/config.json"):
            copy_config()

        # Assert correct calls
        mock_resource_filename.assert_called_once_with("runmd", "config.json")
        mock_makedirs.assert_not_called()
        mock_copy.assert_not_called()
        mock_print.assert_called_once_with("Configuration file already exists at mock_dest_path/config.json.")

    @patch('pkg_resources.resource_filename')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.copy')
    @patch('builtins.print')
    def test_copy_config_error_locating_file(self, mock_print, mock_copy, mock_makedirs, mock_exists, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.side_effect = Exception("File not found")

        with patch('os.path.expanduser', return_value="mock_dest_path"):
            copy_config()

        # Assert correct calls
        mock_resource_filename.assert_called_once_with("runmd", "config.json")
        mock_makedirs.assert_not_called()
        mock_copy.assert_not_called()
        mock_print.assert_called_once_with("Error locating the config file: File not found")


    def test_validate_config_valid(self):
        config = {
            "python": {
                "command": "python3",
                "options": ["-c"]
            },
            "ruby": {
                "command": "ruby",
                "options": ['-e']
            }
        }
        try:
            validate_config(config)
        except ValueError:
            self.fail("validate_config raised ValueError unexpectedly.")

    def test_validate_config_invalid_type(self):
        config = {
            "python": {
                "command": "python3",
                "options": ["-c"]
            },
            "ruby": "invalid type"
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(str(context.exception), "Config for language 'ruby' should be a dictionary.")

    def test_validate_config_missing_command(self):
        config = {
            "python": {
                "command": "python3",
                "options": ["-c"]
            },
            "ruby": {
                "options": ['-e']
            }
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(str(context.exception), "Config for language 'ruby' is missing 'command' field.")

    def test_validate_config_missing_options(self):
        config = {
            "python": {
                "command": "python3",
                "options": ["-c"]
            },
            "ruby": {
                "command": "ruby"
            }
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(str(context.exception), "Config for language 'ruby' is missing 'options' field.")

    def test_load_config_invalid_path(self):
        path = "./tests/no_config.json"
        with self.assertRaises(FileNotFoundError) as context:
            _ = load_config(path)
        self.assertEqual(str(context.exception), f"Configuration file not found at {path}")

    def test_get_languages(self):
        config = {
            "python": {
                "command": "python3",
                "options": ["-c"]
            },
            "ruby": {
                "command": "ruby",
                "options": ['-e']
            }
        }
        languages = get_languages(config)
        self.assertListEqual(["python", "ruby"], languages)