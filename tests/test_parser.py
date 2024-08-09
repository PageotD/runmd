import unittest
from runmd.parser import parse_markdown

class TestRunmdParser(unittest.TestCase):

    def test_parse_markdown(self):
        file_path = "tests/test_markdown.md"
        languages = ["python", "ruby"]
        expected = [
            ('hello-python', 'python', '# run with runmd run hello-python\nprint("Hello from Python!")', True), 
            ('hello-ruby', 'ruby', '# run with runmd run hello-ruby\nputs "Hello from Ruby!"', True)
            ]
        code_blocks = parse_markdown(file_path, languages)
        self.assertListEqual(code_blocks, expected)