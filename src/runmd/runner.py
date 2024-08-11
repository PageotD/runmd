import subprocess
import sys
import os

def run_code_block(name: str, lang: str, code: str, config: dict, env_vars: dict):
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
    print(f"\n\033[1;33m> Running: {name} ({lang})\033[0;0m")

    if lang not in config:
        print(f"Error: Unsupported language '{lang}' for code block '{name}'")
        return

    settings = config[lang]
    command = settings.get("command")
    options = settings.get("options", [])

    # Merge the provided environment variables with the current environment
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    if not command:
        print(f"Error: No command specified for language '{lang}'")
        return

    # Prepare command and arguments based on platform
    if sys.platform == "win32":
        # Windows-specific handling
        process = subprocess.Popen(
            [command] + options + [code],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,  # Windows requires shell=True to run commands
            text=True,
        )
    else:
        # Unix-like systems handling
        process = subprocess.Popen(
            [command] + options + [code],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    try:
        # Execute the code block
        stdout, stderr = process.communicate(input=code, timeout=60)

        if process.returncode != 0:
            print(
                f"Error: Code block '{name}' failed with exit code {process.returncode}"
            )
            print(f"Stderr: {stderr}")
        else:
            print(stdout)

    except subprocess.TimeoutExpired:
        print(f"Error: Code block '{name}' timed out.")
        process.kill()
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")
