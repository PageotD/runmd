# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Configuration Management for the 'runmd' CLI Tool

This module provides functionality for managing the configuration of the 'runmd' CLI tool. It
includes functions for locating, copying, loading, validating, and retrieving configuration
settings.

Functions:
    - get_default_config_path: Return the path to the default configuration file.
    - copy_config: Copy the default configuration file to the user's configuration directory if it
      does not already exist.
    - load_config: Load and return the configuration from the file, raising errors for missing or
      invalid files.
    - validate_config: Validate the loaded configuration to ensure it contains required sections
      and fields.
    - get_all_aliases: Retrieve a list of all language aliases defined in the configuration.
    - get_configuratio:  Load and validate the configuration file.

Attributes:
    - None

This module handles the configuration setup and validation for the 'runmd' CLI tool, ensuring that
users have a correctly configured environment for running and processing code blocks.
"""

import configparser
import importlib.resources
import os
import shutil
from pathlib import Path
from typing import Dict, List

CONFIG_FILE_NAME = "config.ini"
CONFIG_DIR_NAME = "runmd"
REQUIRED_LANG_KEYS = ["aliases", "command", "options"]


def get_default_config_path() -> Path:
    """
    Return the path to the default configuration file.

    Returns:
        Path: Default configuration file path.
    """
    return Path.home() / ".config" / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def copy_config() -> None:
    """Copy the default config to the user's configuration directory."""
    try:
        # Locate the source configuration file
        config_source = importlib.resources.files("runmd") / CONFIG_FILE_NAME

        # Determine the destination configuration file path
        config_dest = get_default_config_path()

        # Create the directory if it does not exist
        config_dest.parent.mkdir(parents=True, exist_ok=True)

        # Copy the configuration file if it does not already exist
        if not config_dest.exists():
            shutil.copy(config_source, config_dest)
            print(f"Configuration file copied to {config_dest}.")
        else:
            print(f"Configuration file already exists at {config_dest}.")

    except Exception as e:
        raise FileNotFoundError(e)


def load_config() -> configparser.ConfigParser:
    """
    Load the configuration file.

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
        raise ValueError(f"Error reading configuration file: {e}") from e

    return config


def _validate_lang_section(section):
    # Define required keys for each language section
    required_keys = ["aliases", "command", "options"]

    # Check for required keys in the section
    for key in required_keys:
        if key not in section:
            raise ValueError(f"Section '{section}' is missing the '{key}' field.")

    # Validate 'aliases' to be a comma-separated list
    aliases = section.get("aliases", "")
    if not isinstance(aliases, str) or not all(
        alias.strip() for alias in aliases.split(",")
    ):
        raise ValueError(
            f"Section '{section}' has an invalid 'aliases' field. \
                It should be a non-empty comma-separated list of strings."
        )

    # Validate 'command' to be a non-empty string
    command = section.get("command", "")
    if not isinstance(command, str) or not command.strip():
        raise ValueError(
            f"Section '{section}' has an invalid 'command' field. It should be a non-empty string."
        )

    # Validate 'options' to be a string
    options = section.get("options", "")
    if not isinstance(options, str):
        raise ValueError(
            f"Section '{section}' has an invalid 'options' field. It should be a string."
        )


def validate_config(config: configparser.ConfigParser) -> None:
    """
    Validate the configuration to ensure it contains required sections and fields.

    Args:
        config (configparser.ConfigParser): Configuration object to validate.
    """

    # Iterate over all sections in the config
    for section in config.sections():
        if section.startswith("lang."):

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
        if section.startswith("lang."):
            # Get aliases for the section
            section_aliases = config[section].get("aliases", "")
            if section_aliases:
                # Split aliases by comma and strip whitespace
                aliases.extend(alias.strip() for alias in section_aliases.split(","))

    return aliases


def get_configuration() -> configparser.ConfigParser:
    """
    Load and validate the configuration file.

    If the config file doesn't exist, it creates a default one.
    Then it loads the config and validates it.

    Returns:
        configparser.ConfigParser: Loaded and validated configuration object.

    Raises:
        FileNotFoundError: If the config file cannot be created or accessed.
        ValueError: If the configuration is invalid.
    """
    config_path = get_default_config_path()

    if not os.path.exists(config_path):
        try:
            copy_config()
        except Exception as e:
            raise FileNotFoundError(
                f"Failed to create config file at {config_path}: {str(e)}"
            )

    try:
        config = load_config()
        validate_config(config)
        return config
    except configparser.Error as e:
        raise ValueError(f"Invalid configuration: {str(e)}")
