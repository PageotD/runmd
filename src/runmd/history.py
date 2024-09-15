# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
History Management for the 'runmd' CLI Tool

This module provides functionality for managing command history in the 'runmd' CLI tool. It allows
for reading from, writing to, and updating the command history file, as well as printing and
cleaning command entries.

Functions:
    - get_history_path: Return the path to the command history file.
    - read_history: Read and return the command history from the file.
    - write_history: Write the command history to the file.
    - update_history: Update the history with a new command and manage history size.
    - print_history: Print the stored command history.
    - clean_command: Clean up the command string by removing unnecessary parts before the 'runmd'
      command.

Attributes:
    - None

This module handles the persistent storage of command history, ensuring that the history file is
updated accurately and can be used to track previous commands.
"""

import datetime
import json
import os
import re
import tempfile
from pathlib import Path


def get_history_path() -> Path:
    """
    Return the path to the runmd command history file.

    Returns:
        Path: The path to the history file.
    """
    return Path.home() / ".config" / "runmd" / "history.json"


def load_history() -> list:
    """
    Load the command history from the file.

    Returns:
        list[dict]: A list of dictionaries representing command history.
    """
    hist_path = get_history_path()

    if not hist_path.exists():
        return []

    try:
        with open(hist_path, "r") as fhistory:
            history = json.load(fhistory)
    except (json.JSONDecodeError, IOError) as e:
        raise ValueError(f"Error reading history file: {e}") from e

    return history


def write_history(history: list) -> None:
    """
    Write the command history to the history file.

    Args:
        history(list[dict]): The command history to be written.
    """
    hist_path = get_history_path()
    hist_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    try:
        # Write to a temporary file first to ensure atomic write
        with tempfile.NamedTemporaryFile(
            "w", dir=hist_path.parent, delete=False
        ) as tmpfile:
            json.dump(history, tmpfile, indent=2)
            tempname = tmpfile.name
        # Rename the temporary file to the final file
        Path(tempname).replace(hist_path)
    except IOError as e:
        print(f"Error writing history file: {e}")


def update_history(history: list, histsize: int, command: str, success: bool) -> list:
    """
    Update the history list with a new command.

    Args:
        history(list[dict]): The current history list.
        histsize(int): Maximum number of commands to remember.
        command(str): The command to add to the history.
        success(bool): Whether the command was successful or not.

    Returns:
        list[dict]: The updated history list.
    """
    # Get the next command ID
    next_id = history[-1]["id"] + 1 if history else 0

    # Append the new command to history
    if success:
        status = "SUCCESS"
    else:
        status = "FAIL"

    history.append(
        {
            "id": next_id,
            "date": datetime.datetime.now().isoformat(),  # Store date as ISO formatted string
            "root": os.getcwd(),
            "command": clean_command(command),
            "status": status,
        }
    )

    # Limit the history size
    return history[-histsize:]


def print_history(history: list) -> None:
    """
    Print the last N commands stored in the history.

    Args:
        history(list[dict]): The command history to print.
    """
    for element in history:
        print(
            f"{element['id']} {element['date']} {element['root']} {element['command']} {element['status']}"
        )


def clean_command(command: str) -> str:
    """
    Clean the command by removing everything before the last 'runmd'.

    Args:
        command (str): the command to clean

    Returns:
        str: The cleaned commands.
    """
    # Regex to match everything before the last occurrence of 'runmd'
    cleaned_command = re.sub(r"^.*\b(runmd\b.*)", r"\1", command)

    return cleaned_command
