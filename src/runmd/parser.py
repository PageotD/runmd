import re

def parse_markdown(file_path: str, languages: list, blocklist: list) -> list:
    """
    Parse the Markdown file to extract code blocks with names.

    Args:
        file_path (str): Path to the Markdown file.
        languages (list): List of valid languages.

    Returns:
        list: List of tuples containing code block information.
    """
    pattern = re.compile(
        rf"```({('|').join(languages)}) \{{name=(.*?)(?:,\s*tag=(.*?))?\}}\s*([\s\S]*?)\s*```", re.DOTALL
    )


    try:
        with open(file_path, "r") as file:
            content = file.read()

        matches = pattern.findall(content)
        for lang, name, tag, code in matches:
            #code_blocks.append((name.strip(), lang, code.strip(), lang in languages))
            blocklist.append({
                "name": name.strip(),
                "tag": tag,
                "file": file_path,
                "lang": lang,
                "code": code.strip(),
                "exec": lang in languages
            })

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return blocklist
