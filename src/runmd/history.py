from pathlib import Path
import json
import datetime
import tempfile
import re

def get_history_path() -> Path:
    """
    Return the path to the runmd command history file.

    Returns:
        Path: The path to the history file.
    """
    return Path.home() / ".config" / "runmd" / "history.json"

def read_history() -> list:
    """
    Read the command history from the file.

    Returns:
        list[dict]: A list of dictionaries representing command history.
    """
    hist_path = get_history_path()
    
    if not hist_path.exists():
        return []

    try:
        with open(hist_path, 'r') as fhistory:
            history = json.load(fhistory)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading history file: {e}")
        return []
    
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
        with tempfile.NamedTemporaryFile('w', dir=hist_path.parent, delete=False) as tmpfile:
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

    Returns:
        list[dict]: The updated history list.
    """
    # Get the next command ID
    next_id = history[-1]['id'] + 1 if history else 0

    # Append the new command to history
    if success:
        status = "SUCCESS"
    else:
        status = "FAIL"

    history.append({
        "id": next_id,
        "date": datetime.datetime.now().isoformat(),  # Store date as ISO formatted string
        "command": clean_command(command),
        "status": status
    })

    # Limit the history size
    return history[-histsize:]

def print_history(history: list) -> None:
    """
    Print the last N commands stored in the history.

    Args:
        history(list[dict]): The command history to print.
    """
    for element in history:
        print(f"{element['id']} {element['date']} {element['command']} {element['status']}")

def clean_command(command: str) -> str:
    """
    Clean the command by removing everything before the last 'runmd'.
    
    Args:
        command (str): the command to clean
    
    Returns:
        str: The cleaned commands.
    """
    # Regex to match everything before the last occurrence of 'runmd'
    cleaned_command = re.sub(r'^.*\b(runmd\b.*)', r'\1', command)
        
    return cleaned_command
