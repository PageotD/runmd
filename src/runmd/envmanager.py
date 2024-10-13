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

import os

import dotenv


def load_dotenv():
    """
    Load the .runenv file

    Returns:
        dict: The contents of the .runenv file
    """
    runenv = {}
    if os.path.exists(".runenv"):
        with open(".runenv") as f:
            runenv = dotenv.dotenv_values(f)
    return runenv


def load_process_env():
    """
    Load the process environment variables

    Returns:
        dict: The process environment variables
    """
    process_env = os.environ.copy()
    return process_env


def update_runenv(runenv, userenv):
    """
    Update the .runenv file with the user environment variables

    Args:
        runenv (dict): The contents of the .runenv file
        userenv (dict): The user environment variables

    Returns:
        dict: The updated .runenv file
    """
    for key, value in userenv.items():
        runenv[key] = value
    return runenv


def write_runenv(runenv):
    """
    Write the .runenv file with the user environment variables

    Args:
        runenv (dict): The contents of the .runenv file
    """
    with open(".runenv", "w") as f:
        for key, value in runenv.items():
            dotenv.set_key(f, key, value)
