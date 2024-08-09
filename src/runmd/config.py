import os
import json


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

    validate_config(config)
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
