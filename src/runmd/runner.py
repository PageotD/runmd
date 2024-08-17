import subprocess
import sys
import os
import configparser

def run_code_block(name: str, lang: str, code: str, tag: str, config: configparser.ConfigParser, env_vars: dict):
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

    #if lang not in config:
    #    print(f"Error: Unsupported language '{lang}' for code block '{name}'")
    #    return

    for section in config.sections():
        if section.startswith('lang.'):
            section_aliases = config[section].get('aliases', '')
            if lang in section_aliases:
                command = config[section].get('command', '').split()
                options = config[section].get('options', '').split()

    # Merge the provided environment variables with the current environment
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    if not command:
        print(f"Error: No command specified for language '{lang}'")
        return

    try:
        # Prepare command and arguments based on platform
        if sys.platform == "win32":
            active_shell = True
        else:
            active_shell = False

        process = subprocess.Popen(
            command + options + [code],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=active_shell
        )

        while True:
            output = process.stdout.readline().rstrip().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")
