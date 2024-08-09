import re


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
    pattern = re.compile(
        rf"```({('|').join(languages)}) \{{name=(.*?)\}}\n(.*?)\n```", re.DOTALL
    )

    try:
        with open(file_path, "r") as file:
            content = file.read()

        matches = pattern.findall(content)
        for lang, name, code in matches:
            code_blocks.append((name.strip(), lang, code.strip(), lang in languages))

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return code_blocks
