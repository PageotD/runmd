# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Markdown Code Block Parser

This module provides functions to parse Markdown files and extract code blocks based on specific
patterns. It focuses on identifying code blocks with associated metadata such as language, name,
and tag.

Functions:
    - compile_pattern: Compile a regular expression pattern to match code blocks in Markdown files.
    - parse_markdown: Parse a Markdown file to extract code blocks and their metadata.

The parsing functionality relies on regular expressions to identify and extract code blocks that
include specified languages and metadata. The extracted code blocks are returned as a list of
dictionaries containing relevant information.

Usage:
    - Use `compile_pattern` to create a regular expression pattern for matching code blocks.
    - Use `parse_markdown` to read a Markdown file and extract code blocks based on the compiled
      pattern and provided languages.
"""

import re

class CodeBlock:

    def __init__(self, language: str, name: str, tag: str, code: str):
        self.language = language
        self.name = name
        self.tag = tag
        self.code = code
        self.command = None
        self.options = None


    def instruction(self) -> str:
        return f"{self.command} {self.options} {self.code}"

class MarkdownParser:

    def __init__(self):
        pass

    def compile_pattern(self, languages: list) -> re.Pattern:
        """
        Compile the regular expression pattern for matching code blocks.

        Args:
            languages (List[str]): List of valid languages.

        Returns:
            re.Pattern: Compiled regex pattern for parsing code blocks.
        """
        return re.compile(
            rf"```({('|').join(languages)}) \{{name=(.*?)(?:,\s*tag=(.*?))?\}}\s*([\s\S]*?)\s*```",
            re.DOTALL,
        )


    def detect_shebang(self,content: str) -> str|None:
        """
        Detect the shebang used in the code block.

        Args:
            content (str): The content of the code block.

        Returns:
            str: The shebang used in the code block.
        """
        shebang_pattern = r"^#!\s*(\/usr\/bin\/env\s+)?(\S+)"
        match = re.search(shebang_pattern, content, re.MULTILINE)

        if match:
            return f"{match.group(1)}{match.group(2)}" if match.group(1) else match.group(2) if match else None

        return None


    def parse(self, file_path: str, languages: list) -> list:
        """
        Parse the Markdown file to extract code blocks with names.

        Args:
            file_path (str): Path to the Markdown file.
            languages (list): List of valid languages.

        Returns:
            list: List of CodeBlock objects containing code block information
                or an empty List if file not found.
        """
        pattern = self.compile_pattern(languages)
        try:
            with open(file_path, "r") as file:
                content = file.read()

            matches = pattern.findall(content)

            code_blocks = []
            for lang, name, tag, code in matches:
                shebang = self.detect_shebang(code)
                code_block = CodeBlock(lang, name.strip(), tag, code.strip())
                if shebang:
                    code_block.name = shebang
                code_blocks.append(code_block)

            return code_blocks

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

        return []
