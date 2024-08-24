"""
Code Block Execution

This module provides functionality for executing code blocks extracted from Markdown files.
It handles the execution of code using configurations defined for different programming languages.

Functions:
    - run_code_block: Execute a specific code block using the command and options defined in the
      configuration file.

The `run_code_block` function takes the code block's name, language, code, and associated metadata,
along with a configuration dictionary and environment variables. It then runs the code block using
the appropriate command for the specified language, capturing and printing the output.

Usage:
    - Use `run_code_block` to execute code blocks with the provided configuration and environment
      settings. The function handles command preparation, execution, and output streaming, and it
      prints the output directly to the console.

Error Handling:
    - If the specified language is not supported or no command is defined, an error message is
      printed.
    - Any exceptions during the execution of the code block are caught and reported.
"""

import subprocess
import sys
import os
import configparser


def run_code_block(
    name: str,
    lang: str,
    code: str,
    tag: str,
    config: configparser.ConfigParser,
    env_vars: dict,
):
    """
    Execute the specified code block using configuration.

    Args:
        name (str): Name of the code block.
        lang (str): Programming language or script type.
        code (str): The code to execute.
        config (dict): Configuration dictionary containing commands and options.

    Returns:
        None
    """
    print(f"\n\033[1;33m> Running: {name} ({lang}) {tag}\033[0;0m")

    command = None
    options = None

    for section in config.sections():
        if section.startswith("lang."):
            section_aliases = config[section].get("aliases", "")
            if lang in section_aliases:
                command = config[section].get("command", "").split()
                options = config[section].get("options", "").split()

    # Merge the provided environment variables with the current environment
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    if not command:
        print(f"Error: No command specified for language '{lang}'")
        return None

    try:
        # Prepare command and arguments based on platform
        active_shell = sys.platform == "win32"

        process = subprocess.Popen(
            command + options + [code],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=active_shell,
        )

        while True:
            output = process.stdout.readline().rstrip().decode("utf-8")
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())

        return process.returncode == 0

    except Exception as e:

        print(f"Error: Code block '{name}' failed with exception: {e}")
        return False
