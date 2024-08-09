import unittest
from runmd.config import load_config, validate_config, get_default_config_path, get_languages

class TestRunmdConfig(unittest.TestCase):

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