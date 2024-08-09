import argparse
import os
import json
import subprocess
import re

from .config import load_config, get_default_config_path, get_languages


def parse_markdown(file_path: str, languages: list) -> tuple:
    """
    Parse the Markdown file to extract code blocks with names.

    Args:
        file_path (str): Path to the Markdown file.
        languages (list): List of valid languages.

    Returns:
        list: List of tuples containing code block information.
    """
    code_blocks = []
    with open(file_path, "r") as file:
        content = file.read()

    pattern = re.compile(
        rf"```({('|').join(languages)}) \{{name=(.*?)\}}\n(.*?)\n```", re.DOTALL
    )
    matches = pattern.findall(content)

    for lang, name, code in matches:
        code_blocks.append((name.strip(), lang, code.strip(), lang in languages))

    return code_blocks


def list_code_blocks(code_blocks: tuple) -> None:
    """
    List all code block names along with their language.

    Args:
        code_blocks (list): List of tuples containing code block information.
    """
    print("\033[0;31m\u26AC\033[0;0m Available code block names:")
    for name, lang, _, runnable in code_blocks:
        if runnable:
            print(f"\u0020\u0020\033[0;31m-\033[0;0m {name} ({lang})")
        else:
            print(
                f"\u0020\u0020\033[0;31m-\033[0;0m {name} (\033[0;31m{lang}: not configured\033[0;0m)"
            )


def show_code_block(name: str, lang: str, code: str) -> None:
    """
    Display the code block contents.

    Args:
        name (str): Name of the code block.
        lang (str): Language of the code block.
        code (str): Code block content.
    """
    print(f"\n\033[1;33m> Showing: {name} ({lang})\033[0;0m")
    print(code)


def run_code_block(name: str, lang: str, code: str, config: dict) -> None:
    """
    Execute the specified code block using the configuration.

    Args:
        name (str): Name of the code block.
        lang (str): Language of the code block.
        code (str): Code block content.
        config (dict): Configuration dictionary.
    """
    print(f"\n\033[1;33m> Running: {name} ({lang})\033[0;0m")
    try:
        if lang in config:
            command = config[lang]["command"]
            options = config[lang]["options"]

            process = subprocess.Popen(
                [command] + options + [code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(
                    f"Error: Code block '{name}' failed with exit code {process.returncode}"
                )
                print(f"Stderr: {stderr.decode()}")
            else:
                print(stdout.decode())
        else:
            print(f"Error: Unsupported language '{lang}' for code block '{name}'")
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")


def process_markdown_files(
    directory: str, command: str, block_name: str = None, config: dict = None
) -> None:
    """
    Process all Markdown files in the given directory.

    Args:
        directory (str): Directory to scan for Markdown files.
        command (str): Command to execute ('run', 'ls', or 'show').
        block_name (str, optional): Name of the code block to process. Defaults to None.
        config (dict, optional): Configuration dictionary. Defaults to None.
    """
    languages = get_languages(config)

    for file in os.listdir(directory):
        if file.endswith(".md"):
            file_path = os.path.join(directory, file)
            print(f"\033[0;31m\u26AC\033[0;0m Processing file: {file_path}")

            code_blocks = parse_markdown(file_path, languages)

            if command == "ls":
                list_code_blocks(code_blocks)
            elif command == "show":
                for name, lang, code, _ in code_blocks:
                    if name == block_name:
                        show_code_block(name, lang, code)
            elif command == "run":
                if block_name == "all":
                    for name, lang, code, runnable in code_blocks:
                        if runnable:
                            run_code_block(name, lang, code, config)
                        else:
                            print(
                                f"Error: {lang} is not configured. Please add {lang} to the config file to run this code block."
                            )
                elif block_name:
                    for name, lang, code, runnable in code_blocks:
                        if name == block_name:
                            if runnable:
                                run_code_block(name, lang, code, config)
                            else:
                                print(
                                    f"Error: {lang} is not configured. Please add {lang} to the config file to run this code block."
                                )
                            break
                    else:
                        print(f"Error: Code block with name '{block_name}' not found.")
                else:
                    print("Error: You must provide a code block name or 'all' to run.")
        else:
            print(f"Skipping non-Markdown file: {file}")


def main() -> None:
    """
    Main function to parse arguments and execute commands.
    """
    parser = argparse.ArgumentParser(
        description="Run or list code blocks from Markdown files in the directory."
    )
    parser.add_argument(
        "command",
        choices=["run", "ls", "show"],
        help="Command to run, list or show code blocks.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help='Name of the code block to run (or "all" to run all code blocks).',
    )
    parser.add_argument(
        "--dir", default=".", help="Directory to scan for Markdown files."
    )
    parser.add_argument(
        "--config", default=None, help="Path to the configuration file."
    )

    args = parser.parse_args()

    if args.command in ["run", "show"] and not args.name:
        print("Error: You must provide a code block name or 'all' to run/show.")
        return

    config_path = args.config if args.config else get_default_config_path()
    config = load_config(config_path)

    process_markdown_files(args.dir, args.command, args.name, config)


if __name__ == "__main__":
    main()
