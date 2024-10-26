# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Manage the environment variables

This module provides functionality for managing the environment variables in the .session file
and to copy process environment variables.

Functions:
    - load_dotenv: Load the .session file
    - load_process_env: Load the process environment variables
    - update_runenv: Update the .session file with the user environment variables
    - write_runenv: Write the .session file with the user environment variables
"""

import base64
import os

import dotenv


def load_dotenv():
    """
    Load the .session file

    Returns:
        dict: The contents of the .session file
    """
    if os.path.exists(".session"):
        return dotenv.dotenv_values(".session")
    return {}


def load_process_env():
    """
    Load the process environment variables

    Returns:
        dict: The process environment variables
    """
    process_env = os.environ.copy()
    return process_env


def update_runenv_file(runenv):
    """
    Update the .session file

    Args:
        runenv (dict): The contents of the .session file
    """
    for key, value in runenv.items():
        encoded_value = base64.b64encode(value.encode("utf-8"))
        dotenv.set_key(".session", key, encoded_value.decode("utf-8"))


def merge_envs(env, runenv):
    """
    Merge the user environment variables with the .session file

    Args:
        env (dict): The user environment variables
        runenv (dict): The contents of the .session file
    """
    for key, value in runenv.items():
        decoded_value = base64.b64decode(value).decode("utf-8")
        env[key] = decoded_value
