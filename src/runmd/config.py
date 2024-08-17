"""
config.py

Description:
The `config.py` module handles configuration-related tasks for the 'runmd' package. It includes
functionalities to copy a default configuration file to the user's home directory, load and 
validate the configuration file, and retrieve information about configured scripting languages.

Functions:
- get_default_config_path: Returns the path to the default configuration file for 'runmd'.
- copy_config: Copies the default configuration file to the user's configuration directory if it 
  does not already exist.
- load_config: Loads the configuration file from a specified path.
- validate_config: Validates the configuration dictionary to ensure it contains required fields.
- get_all_aliases: Retrieve a list of all language aliases from the configuration.
"""

import shutil
import pkg_resources
import configparser
from pathlib import Path
from typing import List

def get_default_config_path() -> Path:
    """
    Return the path to the default configuration file.

    Returns:
        Path: Default configuration file path.
    """
    return Path.home() / ".config" / "runmd" / "config.ini"

def copy_config() -> None:
    """Copy the default config to the user's configuration directory."""
    try:
        # Locate the source configuration file
        config_source = pkg_resources.resource_filename("runmd", "config.ini")
        config_source_path = Path(config_source)
    except Exception as e:
        print(f"Error locating the config file: {e}")
        return

    # Determine the destination configuration file path
    config_dest = get_default_config_path()

    # Create the directory if it does not exist
    config_dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy the configuration file if it does not already exist
    if not config_dest.exists():
        shutil.copy(config_source_path, config_dest)
        print(f"Configuration file copied to {config_dest}.")
    else:
        print(f"Configuration file already exists at {config_dest}.")


def load_config() -> configparser.ConfigParser:
    """
    Load and validate the configuration file.

    Returns:
        configparser.ConfigParser: Loaded configuration object.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        ValueError: If the configuration file is invalid.
    """
    config_path = get_default_config_path()

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    config = configparser.ConfigParser()
    
    try:
        config.read(config_path)
    except configparser.Error as e:
        raise ValueError(f"Error reading configuration file: {e}")

    return config

def _validate_lang_section(section):
    # Define required keys for each language section
    required_keys = ['aliases', 'command', 'options']

    # Check for required keys in the section
    for key in required_keys:
        if key not in section:
            raise ValueError(f"Section '{section}' is missing the '{key}' field.")
    
    # Validate 'aliases' to be a comma-separated list
    aliases = section.get('aliases', '')
    if not isinstance(aliases, str) or not all(alias.strip() for alias in aliases.split(',')):
        raise ValueError(f"Section '{section}' has an invalid 'aliases' field. It should be a non-empty comma-separated list of strings.")
    
    # Validate 'command' to be a non-empty string
    command = section.get('command', '')
    if not isinstance(command, str) or not command.strip():
        raise ValueError(f"Section '{section}' has an invalid 'command' field. It should be a non-empty string.")
    
    # Validate 'options' to be a string
    options = section.get('options', '')
    if not isinstance(options, str):
        raise ValueError(f"Section '{section}' has an invalid 'options' field. It should be a string.")


def validate_config(config: configparser.ConfigParser) -> None:
    """
    Validate the configuration to ensure it contains required sections and fields.

    Args:
        config (configparser.ConfigParser): Configuration object to validate.
    """

    # Iterate over all sections in the config
    for section in config.sections():
        if section.startswith('lang.'):

            # Validate language sections
            _validate_lang_section(config[section])

def get_all_aliases(config: configparser.ConfigParser) -> List[str]:
    """
    Retrieve a list of all language aliases from the configuration.

    Args:
        config (configparser.ConfigParser): Configuration object to read aliases from.

    Returns:
        List[str]: List of all aliases across all language sections.
    """
    aliases = []

    # Iterate over all sections in the config
    for section in config.sections():
        if section.startswith('lang.'):
            # Get aliases for the section
            section_aliases = config[section].get('aliases', '')
            if section_aliases:
                # Split aliases by comma and strip whitespace
                aliases.extend(alias.strip() for alias in section_aliases.split(','))

    return aliases

