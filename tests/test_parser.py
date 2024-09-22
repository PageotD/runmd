import unittest
import re
from runmd.parser import compile_pattern, parse_markdown

class TestRunmdParser(unittest.TestCase):

    # --------------------------------------------------
    # >> COMPILE_PATTERN
    # --------------------------------------------------

    def test_compile_pattern(self):
        languages = ["python", "ruby"]
        result = compile_pattern(languages)
        expected = re.compile('```(python|ruby) \\{name=(.*?)(?:,\\s*tag=(.*?))?\\}\\s*([\\s\\S]*?)\\s*```', re.DOTALL)
        self.assertEqual(expected, result)

    # --------------------------------------------------
    # >> PARSE_MARKDOWN
    # --------------------------------------------------
    
    def test_parse_markdown(self):
        file_path = "tests/test_markdown.md"
        languages = ["python", "ruby"]
        blocklist = []
        expected = [
            {'name': 'hello-python', 'tag': 'sometag', 'file': file_path, 'lang':'python', 'code': '# run with runmd run hello-python\nprint("Hello from Python!")', 'exec': True}, 
            {'name': 'hello-ruby', 'tag': '', 'file': file_path, 'lang': 'ruby', 'code': '# run with runmd run hello-ruby\nputs "Hello from Ruby!"', 'exec': True}
            ]
        blocklist = parse_markdown(file_path, languages)
        self.assertListEqual(blocklist, expected)