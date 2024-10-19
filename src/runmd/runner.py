# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Code Block Execution

This module provides functionality for executing code blocks extracted from Markdown files.
It handles the execution of code using configurations defined for different programming languages.

Functions:
    - run_code_block: Execute a specific code block using the command and options defined in the
      configuration file.
    - detect_shebang: Check if the first line of the code block contains a shebang #! and return it
      has `command` else return command from config.ini
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

import configparser
import os
import subprocess
import sys
import tempfile

from .envmanager import load_dotenv, merge_envs, update_runenv_file


def detect_shebang(code: str, section: str, config: configparser.ConfigParser):
    """
    Check if the first line of the code block contains a shebang #!

    Args:
        code(str): The code to execute

    Returns:
        list: The command to execute the code block or None
    """
    split_code = code.split("\n")
    if split_code[0].startswith("#!"):
        return [split_code[0].replace("#!", "")]
    return config[section].get("command", "").split()


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
                command = detect_shebang(code, section, config)
                options = config[section].get("options", "").split()

    # Merge the provided environment variables with the current environment
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    runenv = load_dotenv()
    merge_envs(env, runenv)

    if not command:
        print(f"Error: No command specified for language '{lang}'")
        return None

    try:
        # Prepare command and arguments based on platform
        active_shell = sys.platform == "win32"

        # Keep the solution to put the script in a temporary file
        # --------------------------------------------------------
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".sh") as temp_script:
        #    temp_script.write(code.encode())
        #    temp_script_path = temp_script.name
        # command = [command[0], temp_script_path]  # + command[1:]

        process = subprocess.Popen(
            command + options + [code],
            env=env,
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
            runenv["__"] = output

        update_runenv_file(runenv)

        return process.returncode == 0

    except Exception as e:

        print(f"Error: Code block '{name}' failed with exception: {e}")
        return False
