"""
Manage the environment variables

This module provides functionality for managing the environment variables in the .runenv file
and to copy process environment variables.

Functions:
    - load_dotenv: Load the .runenv file
    - load_process_env: Load the process environment variables
    - update_runenv: Update the .runenv file with the user environment variables
    - write_runenv: Write the .runenv file with the user environment variables
"""

import base64
import os

import dotenv


def load_dotenv():
    """
    Load the .runenv file

    Returns:
        dict: The contents of the .runenv file
    """
    if os.path.exists(".runenv"):
        return dotenv.dotenv_values(".runenv")
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
    Update the .runenv file

    Args:
        runenv (dict): The contents of the .runenv file
    """
    for key, value in runenv.items():
        encoded_value = base64.b64encode(value.encode("utf-8"))
        dotenv.set_key(".runenv", key, encoded_value.decode("utf-8"))


def merge_envs(env, runenv):
    for key, value in runenv.items():
        decoded_value = base64.b64decode(value).decode("utf-8")
        env[key] = decoded_value
