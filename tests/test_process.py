import unittest
import tempfile
import os
from unittest.mock import patch
from runmd.process import process_markdown_files, list_command, show_command, run_command

class TestRunmdProcess(unittest.TestCase):

    @patch('builtins.print')
    def test_list_command(self, mock_print):
        code_blocks = [
            ('block1', 'python', 'print("Hello World")', True),
            ('block2', 'java', 'System.out.println("Hello World");', False),
        ]
        list_command(code_blocks)
        
        expected_output = [
            "\u0020\u0020\033[0;31m-\033[0;0m block1 (python)",
            "\u0020\u0020\033[0;31m-\033[0;0m block2 (\033[0;31mjava: not configured\033[0;0m)"
        ]
        
        # Check if the expected outputs are printed
        calls = [unittest.mock.call(line) for line in expected_output]
        mock_print.assert_has_calls(calls)

    @patch('runmd.process.show_code_block')
    def test_show_command(self, mock_show_code_block):
        code_blocks = [
            ('block1', 'python', 'print("Hello World")', True),
            ('block2', 'java', 'System.out.println("Hello World");', True),
        ]
        show_command(code_blocks, 'block1')
        
        mock_show_code_block.assert_called_once_with('block1', 'python', 'print("Hello World")')

    @patch('builtins.print')
    def test_show_command_not_found(self, mock_print):
        code_blocks = [
            ('block1', 'python', 'print("Hello World")', True),
        ]
        show_command(code_blocks, 'block_not_found')
        
        mock_print.assert_called_once_with("Error: Code block with name 'block_not_found' not found.")

    @patch('runmd.process.run_code_block')
    def test_run_command_env_none(self, mock_run_code_block):
        config = {'python': {'command': 'python', 'options': []}}
        code_blocks = [
            ('block1', 'python', 'print("Hello World")', True),
            ('block2', 'java', 'System.out.println("Hello World");', False),
        ]
        env_vars = {}
        run_command(code_blocks, 'block1', config, env_vars)
        
        # Check that run_code_block is called for block1 only
        mock_run_code_block.assert_called_once_with('block1', 'python', 'print("Hello World")', config, {})

    @patch('builtins.print')
    def test_run_command_block_not_found(self, mock_print):
        config = {'python': {'command': 'python', 'options': []}}
        code_blocks = [
            ('block1', 'python', 'print("Hello World")', True),
        ]
        env_vars = {}
        run_command(code_blocks, 'block_not_found', config, env_vars)
        
        mock_print.assert_called_once_with("Error: Code block with name 'block_not_found' not found.")

    @patch('os.listdir')
    @patch('runmd.process.parse_markdown')
    @patch('runmd.process.list_command')
    @patch('runmd.process.show_command')
    @patch('runmd.process.run_command')
    def test_process_markdown_files(self, mock_run_command, mock_show_command, mock_list_command, mock_parse_markdown, mock_listdir):
        # Mock return values and side effects
        mock_listdir.return_value = ['file1.md']
        mock_parse_markdown.return_value = [
            ('block1', 'python', 'print("Hello World")', True),
            ('block2', 'java', 'System.out.println("Hello World");', False),
        ]

        # Create a temporary file to simulate 'file1.md'
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as temp_file:
            temp_file_path = temp_file.name

        try:
            # Test the 'ls' command
            process_markdown_files(temp_file_path, 'list', config={'python': {'command': 'python', 'options': []}})
            mock_list_command.assert_called_once_with(mock_parse_markdown.return_value)

            # Test the 'show' command
            process_markdown_files(temp_file_path, 'show', 'block1', config={'python': {'command': 'python', 'options': []}})
            mock_show_command.assert_called_once_with(mock_parse_markdown.return_value, 'block1')

            # Test the 'run' command
            #process_markdown_files(temp_file_path, 'run', 'block1', config={'python': {'command': 'python', 'options': []}})
            #mock_run_command.assert_called_once_with(mock_parse_markdown.return_value, 'block1', {'python': {'command': 'python', 'options': []}})
            
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)