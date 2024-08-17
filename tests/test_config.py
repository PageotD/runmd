import unittest
from unittest.mock import patch, mock_open
import json
from runmd.config import get_default_config_path, copy_config, load_config, _validate_lang_section, get_all_aliases
import configparser
from pathlib import Path

class TestRunmdConfig(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()

    # --------------------------------------------------
    # >> COPY_CONFIG
    # --------------------------------------------------

    @patch('pkg_resources.resource_filename')
    @patch('shutil.copy')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.print')
    def test_copy_config_success(self, mock_print, mock_mkdir, mock_exists, mock_copy, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.return_value = "/mock/source/config.ini"
        mock_exists.side_effect = [False]  # Simulate the file does not exist

        # Call the function
        copy_config()

        # Verify behavior
        mock_resource_filename.assert_called_once_with("runmd", "config.ini")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_copy.assert_called_once_with(Path("/mock/source/config.ini"), get_default_config_path())
        mock_print.assert_called_once_with(f"Configuration file copied to {get_default_config_path()}.")

    @patch('pkg_resources.resource_filename')
    @patch('shutil.copy')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.print')
    def test_copy_config_file_not_exist(self, mock_print, mock_mkdir, mock_exists, mock_copy, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.return_value = "/mock/source/config.ini"
        mock_exists.side_effect = [False]  # Destination file does not exist

        # Call the function
        copy_config()

        # Verify behavior
        mock_resource_filename.assert_called_once_with("runmd", "config.ini")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_copy.assert_called_once_with(Path("/mock/source/config.ini"), get_default_config_path())
        mock_print.assert_called_once_with(f"Configuration file copied to {get_default_config_path()}.")

    @patch('pkg_resources.resource_filename')
    @patch('shutil.copy')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('builtins.print')
    def test_copy_config_file_exists(self, mock_print, mock_mkdir, mock_exists, mock_copy, mock_resource_filename):
        # Setup mocks
        mock_resource_filename.return_value = "/mock/source/config.ini"
        mock_exists.side_effect = [True]  # Destination file already exists

        # Call the function
        copy_config()

        # Verify behavior
        mock_resource_filename.assert_called_once_with("runmd", "config.ini")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_copy.assert_not_called()  # Should not copy the file
        mock_print.assert_called_once_with(f"Configuration file already exists at {get_default_config_path()}.")

    @patch('pkg_resources.resource_filename', side_effect=Exception("Error locating the config file"))
    @patch('builtins.print')
    def test_copy_config_error_locating_file(self, mock_print, mock_resource_filename):
        # Call the function
        copy_config()

        # Verify behavior
        mock_resource_filename.assert_called_once_with("runmd", "config.ini")
        mock_print.assert_called_once_with("Error locating the config file: Error locating the config file")

    # --------------------------------------------------
    # >> LOAD_CONFIG
    # --------------------------------------------------

    @patch('runmd.config.get_default_config_path')
    @patch('pathlib.Path.exists')
    @patch('configparser.ConfigParser.read')
    def test_load_config_success(self, mock_read, mock_exists, mock_get_default_config_path):
        # Simulate config file exists
        mock_exists.return_value = True
        mock_get_default_config_path.return_value = Path("/mock/path/config.ini")
        mock_read.return_value = True  # Simulate successful read

        # Call the function
        config = load_config()

        # Verify the configuration was read successfully
        mock_exists.assert_called_once()
        self.assertIsInstance(config, configparser.ConfigParser)

    @patch('runmd.config.get_default_config_path')
    @patch('pathlib.Path.exists')
    def test_load_config_file_not_found(self, mock_exists, mock_get_default_config_path):
        # Simulate config file does not exist
        mock_exists.return_value = False
        mock_get_default_config_path.return_value = Path("/mock/path/config.ini")

        # Expect FileNotFoundError to be raised
        with self.assertRaises(FileNotFoundError):
            load_config()

        mock_exists.assert_called_once()

    @patch('runmd.config.get_default_config_path')
    @patch('pathlib.Path.exists')
    @patch('configparser.ConfigParser.read')
    def test_load_config_invalid_file(self, mock_read, mock_exists, mock_get_default_config_path):
        # Simulate config file exists
        mock_exists.return_value = True
        mock_get_default_config_path.return_value = Path("/mock/path/config.ini")
        
        # Simulate an error when reading the config file
        mock_read.side_effect = configparser.Error("Mock parsing error")

        # Expect ValueError to be raised
        with self.assertRaises(ValueError):
            load_config()

        mock_exists.assert_called_once()

    # --------------------------------------------------
    # >> VALIDATE_LANG_SECTION
    # --------------------------------------------------

    def test_validate_lang_section_success(self):
        # Valid section
        section = {
            'aliases': 'python, py',
            'command': 'python3',
            'options': '-c'
        }

        # No exception should be raised for a valid section
        try:
            _validate_lang_section(section)
        except ValueError as e:
            self.fail(f"Unexpected ValueError raised: {e}")

    def test_validate_lang_section_missing_keys(self):
        # Missing 'aliases'
        section = {
            'command': 'python3',
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("missing the 'aliases' field", str(cm.exception))

        # Missing 'command'
        section = {
            'aliases': 'python, py',
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("missing the 'command' field", str(cm.exception))

        # Missing 'options'
        section = {
            'aliases': 'python, py',
            'command': 'python3'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("missing the 'options' field", str(cm.exception))

    def test_validate_lang_section_invalid_aliases(self):
        # Invalid 'aliases': not a string
        section = {
            'aliases': None,
            'command': 'python3',
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("invalid 'aliases' field", str(cm.exception))

        # Invalid 'aliases': empty string
        section = {
            'aliases': '',
            'command': 'python3',
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("invalid 'aliases' field", str(cm.exception))

    def test_validate_lang_section_invalid_command(self):
        # Invalid 'command': not a string
        section = {
            'aliases': 'python, py',
            'command': None,
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("invalid 'command' field", str(cm.exception))

        # Invalid 'command': empty string
        section = {
            'aliases': 'python, py',
            'command': '',
            'options': '-c'
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("invalid 'command' field", str(cm.exception))

    def test_validate_lang_section_invalid_options(self):
        # Invalid 'options': not a string
        section = {
            'aliases': 'python, py',
            'command': 'python3',
            'options': None
        }
        with self.assertRaises(ValueError) as cm:
            _validate_lang_section(section)
        self.assertIn("invalid 'options' field", str(cm.exception))

    # --------------------------------------------------
    # >> GET_ALL_ALIASES
    # --------------------------------------------------

    def test_get_all_aliases_single_section(self):
        # Setup a config with a single section
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')

        # Call the function and check the result
        result = get_all_aliases(self.config)
        expected = ['py', 'python']
        self.assertEqual(result, expected)

    def test_get_all_aliases_multiple_sections(self):
        # Setup a config with multiple sections
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')

        self.config.add_section('lang.bash')
        self.config.set('lang.bash', 'aliases', 'bash')

        self.config.add_section('lang.javascript')
        self.config.set('lang.javascript', 'aliases', 'js, javascript, node')

        # Call the function and check the result
        result = get_all_aliases(self.config)
        expected = ['py', 'python', 'bash', 'js', 'javascript', 'node']
        self.assertEqual(result, expected)

    def test_get_all_aliases_empty_aliases(self):
        # Setup a config with a section but no aliases
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', '')

        # Call the function and check the result
        result = get_all_aliases(self.config)
        expected = []
        self.assertEqual(result, expected)

    def test_get_all_aliases_no_lang_sections(self):
        # Setup a config with no 'lang.' sections
        self.config.add_section('other_section')
        self.config.set('other_section', 'aliases', 'something')

        # Call the function and check the result
        result = get_all_aliases(self.config)
        expected = []  # No aliases should be returned since there are no 'lang.' sections
        self.assertEqual(result, expected)