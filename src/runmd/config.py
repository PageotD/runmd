"""
config.py

Description:
The `config.py` module handles configuration-related tasks for the 'runmd' package. It includes
functionalities to copy a default configuration file to the user's home directory, load and 
validate the configuration file, and retrieve information about configured scripting languages.

Functions:
- copy_config: Copies the default configuration file to the user's configuration directory if it 
  does not already exist.
- load_config: Loads and validates the configuration file from a specified path.
- validate_config: Validates the configuration dictionary to ensure it contains required fields 
  and has correct types.
- get_default_config_path: Returns the path to the default configuration file for 'runmd'.
- get_languages: Returns a list of languages configured in the provided configuration dictionary.

"""

import os
import json
import shutil
import pkg_resources


def copy_config():
    """Copy the default config to the user's configuration directory."""
    try:
        config_source = pkg_resources.resource_filename("runmd", "config.json")
    except Exception as e:
        print(f"Error locating the config file: {e}")
        return

    config_dest = os.path.expanduser("~/.config/runmd/config.json")

    if not os.path.exists(os.path.dirname(config_dest)):
        os.makedirs(os.path.dirname(config_dest))

    if not os.path.exists(config_dest):
        shutil.copy(config_source, config_dest)
        print(f"Configuration file copied to {config_dest}.")
    else:
        print(f"Configuration file already exists at {config_dest}.")


def load_config(config_path: str) -> dict:
    """
    Load and validate the configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Loaded configuration dictionary.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        ValueError: If the configuration file is invalid.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, "r") as file:
        config = json.load(file)

    return config


def validate_config(config: dict) -> None:
    """
    Validate the configuration to ensure it contains required fields.

    Args:
        config (dict): Configuration dictionary to validate.

    Raises:
        ValueError: If the configuration is missing required fields or has invalid types.
    """
    required_keys = ["command", "options"]
    for lang, settings in config.items():
        if not isinstance(settings, dict):
            raise ValueError(f"Config for language '{lang}' should be a dictionary.")
        for key in required_keys:
            if key not in settings:
                raise ValueError(
                    f"Config for language '{lang}' is missing '{key}' field."
                )


def get_default_config_path() -> str:
    """
    Return the path to the default configuration file.

    Returns:
        str: Default configuration file path.
    """
    return os.path.expanduser("~/.config/runmd/config.json")


def get_languages(config: dict) -> list:
    """
    Return the list of configured scripting languages.

    Args:
        config (dict): Configuration dictionary.

    Returns:
        list: List of languages configured in the config.
    """
    return list(config.keys())
