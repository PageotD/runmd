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
    - get_configuration:  Load and validate the configuration file.

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
import functools

CONFIG_FILE_NAME = "config.ini"
CONFIG_DIR_NAME = "runmd"
REQUIRED_LANG_KEYS = ["aliases", "command", "options"]

class ConfigLoader:
    def __init__(self):
        self.default_config_path = Path.home() / ".config" / CONFIG_DIR_NAME / CONFIG_FILE_NAME
        self.config = self._get_config()

    @functools.cache
    def _get_config(self) -> configparser.ConfigParser:
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
        if not os.path.exists(self.default_config_path):
            try:
                self._copy_config()
            except Exception as e:
                raise FileNotFoundError(
                    f"Failed to create config file at {self.default_config_path}: {str(e)}"
                )

        try:
            config = self._load_config()
            validate_config(config)
            return config
        except configparser.Error as e:
            raise ValueError(f"Invalid configuration: {str(e)}")


    def _load_config(self) -> configparser.ConfigParser:
        """
        Load the configuration file.

        Returns:
            configparser.ConfigParser: Loaded configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            ValueError: If the configuration file is invalid.
        """
        config_path = self.default_config_path

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at {config_path}")

        config = configparser.ConfigParser()
        if not config.read(config_path):
            raise ValueError(f"Error reading configuration file at {config_path}")

        return config

    def _copy_config(self) -> None:
        """Copy the default config to the user's configuration directory."""
        try:
            # Locate the source configuration file
            config_source = importlib.resources.files("runmd") / CONFIG_FILE_NAME

            # Determine the destination configuration file path
            config_dest = self.default_config_path

            # Create the directory if it does not exist
            config_dest.parent.mkdir(parents=True, exist_ok=True)

            # Copy the configuration file if it does not already exist
            if not config_dest.exists():
                shutil.copy(str(config_source), str(config_dest))
                print(f"Configuration file copied to {config_dest}.")
            else:
                print(f"Configuration file already exists at {config_dest}.")

        except Exception as e:
            raise FileNotFoundError(e)


    def get_all_aliases(self) -> List[str]:
        """
        Retrieve a list of all language aliases from the configuration.

        Args:
            config (configparser.ConfigParser): Configuration object to read aliases from.

        Returns:
            List[str]: List of all aliases across all language sections.
        """
        aliases = []

        # Iterate over all sections in the config
        for section in self.config.sections():
            if section.startswith("lang."):
                # Get aliases for the section
                section_aliases = self.config[section].get("aliases", "")
                if section_aliases:
                    # Split aliases by comma and strip whitespace
                    aliases.extend(alias.strip() for alias in section_aliases.split(","))

        return aliases

    def find_language(self, alias: str) -> str:
        """
        Find the language associated with a given alias.

        Args:
            alias (str): The alias to search for.

        Returns:
            str: The language associated with the alias, or None if not found.
        """
        lang_section = next(
            (
                section
                for section in self.config.sections()
                if section.startswith("lang.")
                   and alias in self.config[section].get("aliases", "").split(",")
            ),
            None,
        )
        return lang_section.split(".")[1]

    def get_language_options(self, language: str) -> List[str]:
        """
        Get the options for a specific language.

        Args:
            language: The language to get options for.

        Returns:
            Dict[str, str]: A dictionary of options for the specified language.
        """
        return self.config[f"lang.{language}"].get("options", "").split()

    def _validate_lang_section(self, section):
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


    def _validate_config(self, config: configparser.ConfigParser) -> None:
        """
        Validate the configuration to ensure it contains required sections and fields.

        Args:
            config (configparser.ConfigParser): Configuration object to validate.
        """

        # Iterate over all sections in the config
        for section in config.sections():
            if section.startswith("lang."):

                # Validate language sections
                self._validate_lang_section(config[section])