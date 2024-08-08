import argparse
import os
import json
import subprocess
import sys
import re

def load_config(config_path):
    """Load the configuration file."""
    with open(config_path, 'r') as file:
        return json.load(file)

def get_default_config_path():
    """Return the path to the default configuration file."""
    return os.path.expanduser('~/.config/runmd/config.json')

def parse_markdown(file_path):
    """Parse the Markdown file to extract code blocks with names."""
    code_blocks = []
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to match code blocks with names
    pattern = re.compile(r'```(sh|python|ruby|javascript|perl) \{name=(.*?)\}\n(.*?)\n```', re.DOTALL)
    matches = pattern.findall(content)

    for lang, name, code in matches:
        code_blocks.append((name.strip(), lang, code.strip()))
    
    return code_blocks

def list_code_blocks(code_blocks):
    """List all the code block names."""
    print("\033[0;31m\u26AC\033[0;0m Available code block names:")
    for name, _, _ in code_blocks:
        print(f"\u0020\u0020\033[0;31m-\033[0;0m {name}")

def show_code_block(name, lang, code, config):
    print(f"\n\033[1;33m> Showing: {name} ({lang})\033[0;0m")
    try:
        print(code)
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")

def run_code_block(name, lang, code, config):
    """Execute the specified code block using configuration."""
    print(f"\n\033[1;33m> Running: {name} ({lang})\033[0;0m")
    try:
        if lang in config:
            command = config[lang]["command"]
            options = config[lang]["options"]

            process = subprocess.Popen([command] + options + [code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Error: Code block '{name}' failed with exit code {process.returncode}")
                print(f"Stderr: {stderr.decode()}")
            else:
                print(stdout.decode())
        else:
            print(f"Error: Unsupported language '{lang}' for code block '{name}'")
    except Exception as e:
        print(f"Error: Code block '{name}' failed with exception: {e}")

def process_markdown_files(directory, command, block_name=None, config=None):
    """Process all Markdown files in the given directory (not subdirectories)."""
    for file in os.listdir(directory):
        if file.endswith(".md"):
            file_path = os.path.join(directory, file)
            print(f"\033[0;31m\u26AC\033[0;0m Processing file: {file_path}")
            code_blocks = parse_markdown(file_path)
            
            if command == 'ls':
                list_code_blocks(code_blocks)
            elif command == 'show':
                for name, lang, code in code_blocks:
                    if name == block_name:
                        show_code_block(name, lang, code, config)
            elif command == 'run':
                if block_name == 'all':
                    for name, lang, code in code_blocks:
                        run_code_block(name, lang, code, config)
                elif block_name:
                    for name, lang, code in code_blocks:
                        if name == block_name:
                            run_code_block(name, lang, code, config)
                            break
                    else:
                        print(f"Error: Code block with name '{block_name}' not found.")
                else:
                    print("Error: You must provide a code block name or 'all' to run.")

def main():
    parser = argparse.ArgumentParser(description='Run or list code blocks from Markdown files in the directory.')
    parser.add_argument('command', choices=['run', 'ls', 'show'], help='Command to run, list or show code blocks.')
    parser.add_argument('name', nargs='?', help='Name of the code block to run (or "all" to run all code blocks).')
    parser.add_argument('--dir', default='.', help='Directory to scan for Markdown files.')
    parser.add_argument('--config', default=None, help='Path to the configuration file.')

    args = parser.parse_args()
    
    if args.command == 'run' and not args.name:
        print("Error: You must provide a code block name or 'all' to run.")
        return
    
    if args.command == 'show' and not args.name:
        print("Error: You must provide a code block name or 'all' to run.")
        return
    
    config_path = args.config if args.config else get_default_config_path()
    config = load_config(config_path)
    process_markdown_files(args.dir, args.command, args.name, config)

if __name__ == '__main__':
    main()
