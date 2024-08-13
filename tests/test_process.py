import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from runmd.process import process_markdown_files, list_command, show_code_block, show_command, run_command

class TestMarkdownProcessing(unittest.TestCase):

    @patch('runmd.parser.parse_markdown')
    @patch('runmd.config.get_languages')
    def test_process_markdown_files(self, mock_get_languages, mock_parse_markdown):
        # Setup mock
        mock_get_languages.return_value = ["python"]
        mock_parse_markdown.return_value = [{'name': 'hello-python', 'tag': 'sometag','lang': 'python', 'file': Path('tests/test_markdown.md'), 'code': 'print("Hello World")', 'exec': True}]
        
        config = {"python": {"command": "python3", "options": ["-c"]}}

        # Test function
        result = process_markdown_files('tests/test_markdown.md', config)
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'hello-python')


    @patch('builtins.print')
    def test_list_command(self, mock_print):
        blocklist = [{'name': 'test_block',  'tag': 'sometag','lang': 'python', 'file': Path('test.md')}]
        
        # Call the function to be tested
        list_command(blocklist)
        
        # Get all print calls
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Define the expected substrings
        expected_substrings = ['NAME', 'LANG', 'FILE', 'TAG', 'test_block', 'python', 'test.md', 'sometag']
        
        # Check if each expected substring is present in the printed output
        for substring in expected_substrings:
            self.assertTrue(any(substring in output for output in print_calls), f"Expected '{substring}' in the output but it was not found.")

    @patch('runmd.process.show_code_block')
    @patch('builtins.print')
    def test_show_command(self, mock_print, mock_show_code_block):
        blocklist = [{'name': 'test_block', 'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")'}]
        
        show_command(blocklist, 'test_block')
        
        mock_show_code_block.assert_called_once_with('test_block', 'python', 'print("Hello World")', 'sometag')
        mock_print.assert_not_called()

    @patch('runmd.process.run_code_block')
    @patch('builtins.print')
    def test_run_command(self, mock_print, mock_run_code_block):
        blocklist = [{'name': 'test_block',  'tag': 'sometag', 'lang': 'python', 'code': 'print("Hello World")', 'exec': True}]
        config = {'python': 'python3'}
        env_vars = {'MY_ENV': 'value'}
        
        run_command(blocklist, 'test_block', config, env_vars)
        
        mock_run_code_block.assert_called_once_with('test_block', 'python', 'print("Hello World")', 'sometag', config, env_vars)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_show_code_block(self, mock_print):
        show_code_block('test_block', 'python', 'print("Hello World")','sometag')
        
        mock_print.assert_any_call("\033[1m\u26AC test_block (python) sometag\033[0m")
        mock_print.assert_any_call("\u0020\u0020\033[90mprint(\"Hello World\")\033[0m")

if __name__ == '__main__':
    unittest.main()
