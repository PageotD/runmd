import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from runmd.process import process_markdown_files, list_command, show_code_block, show_command, run_command
import configparser
from io import StringIO
import re

def strip_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class TestMarkdownProcessing(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()

    # --------------------------------------------------
    # >> PROCESS_MARKDOWN_FILE
    # --------------------------------------------------

    @patch('runmd.parser.parse_markdown')
    @patch('runmd.config.get_all_aliases')
    def test_process_markdown_files(self, mock_get_languages, mock_parse_markdown):
        # Setup mock
        mock_get_languages.return_value = ["python"]
        mock_parse_markdown.return_value = [{'name': 'hello-python', 'tag': 'sometag','lang': 'python', 'file': Path('tests/test_markdown.md'), 'code': 'print("Hello World")', 'exec': True}]
        
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')
        self.config.set('lang.python', 'command', 'python3')
        self.config.set('lang.python', 'options', '-c')

        # Test function
        result = process_markdown_files('tests/test_markdown.md', self.config)
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'hello-python')

    # --------------------------------------------------
    # >> LIST_COMMAND
    # --------------------------------------------------

    @patch('builtins.print')
    def test_list_command(self, mock_print):
        blocklist = [{'name': 'test_block',  'tag': 'sometag','lang': 'python', 'file': Path('test.md')}]
        
        # Call the function to be tested
        list_command(blocklist, 'sometag')
        
        # Get all print calls
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Define the expected substrings
        expected_substrings = ['NAME', 'LANG', 'FILE', 'TAG', 'test_block', 'python', 'test.md', 'sometag']
        
        # Check if each expected substring is present in the printed output
        for substring in expected_substrings:
            self.assertTrue(any(substring in output for output in print_calls), f"Expected '{substring}' in the output but it was not found.")

    # --------------------------------------------------
    # >> SHOW_COMMAND
    # --------------------------------------------------

    @patch('runmd.process.show_code_block')
    @patch('builtins.print')
    def test_show_command(self, mock_print, mock_show_code_block):
        blocklist = [{'name': 'test_block', 'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")'}]
        
        show_command(blocklist, 'test_block')
        
        mock_show_code_block.assert_called_once_with('test_block', 'python', 'print("Hello World")', 'sometag')
        mock_print.assert_not_called()

    @patch('runmd.process.show_code_block')
    @patch('builtins.print')
    def test_show_command_invalid_block_name(self, mock_print, mock_show_code_block):
        blocklist = [{'name': 'test_block', 'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")'}]

        show_command(blocklist, 'fake_block')
        
        mock_print.assert_any_call("Error: Code block with name 'fake_block' not found.")

    # --------------------------------------------------
    # >> RUN_COMMAND
    # --------------------------------------------------

    @patch('runmd.process.run_code_block')
    @patch('builtins.print')
    def test_run_command(self, mock_print, mock_run_code_block):
        blocklist = [{'name': 'test_block',  'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}]
        env_vars = {'MY_ENV': 'value'}
        
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')
        self.config.set('lang.python', 'command', 'python3')
        self.config.set('lang.python', 'options', '-c')

        run_command(blocklist, 'test_block', None, self.config, env_vars)
        
        mock_run_code_block.assert_called_once_with('test_block', 'python', 'print("Hello World")', 'sometag', self.config, env_vars)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_run_command_invalid_block_name(self, mock_print):
        blocklist = [{'name': 'test_block',  'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}]
        env_vars = {'MY_ENV': 'value'}

        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')
        self.config.set('lang.python', 'command', 'python3')
        self.config.set('lang.python', 'options', '-c')

        run_command(blocklist, 'fake_block', None, self.config, env_vars)
        
        mock_print.assert_any_call("Error: Code block with name 'fake_block' not found.")

    @patch('runmd.process.run_code_block')
    @patch('builtins.print')
    def test_run_command_with_tag(self, mock_print, mock_run_code_block):
        blocklist = [{'name': 'test_block1',  'tag': 'sometag1', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}, 
                     {'name': 'test_block2',  'tag': 'sometag2', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}]
        env_vars = {'MY_ENV': 'value'}
        
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')
        self.config.set('lang.python', 'command', 'python3')
        self.config.set('lang.python', 'options', '-c')

        run_command(blocklist, None, 'sometag1', self.config, env_vars)
        
        mock_run_code_block.assert_called_once_with('test_block1', 'python', 'print("Hello World")', 'sometag1', self.config, env_vars)
        mock_print.assert_not_called()

    @patch('runmd.process.run_code_block')
    @patch('builtins.print')
    def test_run_command_invalid_tag(self, mock_print, mock_run_code_block):
        blocklist = [{'name': 'test_block1',  'tag': 'sometag1', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}, 
                     {'name': 'test_block2',  'tag': 'sometag2', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}]
        env_vars = {'MY_ENV': 'value'}
        
        self.config.add_section('lang.python')
        self.config.set('lang.python', 'aliases', 'py, python')
        self.config.set('lang.python', 'command', 'python3')
        self.config.set('lang.python', 'options', '-c')

        run_command(blocklist, None, 'sometag3', self.config, env_vars)
        
        mock_print.assert_any_call("Error: Code block with tag 'sometag3' not found.")

    # --------------------------------------------------
    # >> SHOW_CODE_BLOCK
    # --------------------------------------------------

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_code_block(self, mock_stdout):
        
        name = "example"
        lang = "python"
        code = 'print("Hello, World!")\nfor i in range(5):\n    print(i)'
        tag = "example-tag"

        show_code_block(name, lang, code, tag)

        actual_output = strip_ansi_sequences(mock_stdout.getvalue())

        expected_output = (
            "\n    | print(\"Hello, World!\")\n"
            "    | for i in range(5):\n"
            "    |     print(i)\n\n"
        )

        self.assertEqual(actual_output, expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_code_block_with_invalid_lang(self, mock_stdout):

        name = "example"
        lang = "invalidlang"
        code = 'print("Hello, World!")\nfor i in range(5):\n    print(i)'
        tag = "example-tag"

        show_code_block(name, lang, code, tag)

        expected_output = (
            "Error: Code block 'example' failed with exception: no lexer for alias 'invalidlang' found\n"
            "Original Code:\n"
            "print(\"Hello, World!\")\nfor i in range(5):\n    print(i)\n"
        )

        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
