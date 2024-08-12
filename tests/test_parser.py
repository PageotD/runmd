import unittest
from runmd.parser import parse_markdown

class TestRunmdParser(unittest.TestCase):

    def test_parse_markdown(self):
        file_path = "tests/test_markdown.md"
        languages = ["python", "ruby"]
        blocklist = []
        expected = [
            {'name': 'hello-python', 'file': file_path, 'lang':'python', 'code': '# run with runmd run hello-python\nprint("Hello from Python!")', 'exec': True}, 
            {'name': 'hello-ruby', 'file': file_path, 'lang': 'ruby', 'code': '# run with runmd run hello-ruby\nputs "Hello from Ruby!"', 'exec': True}
            ]
        blocklist = parse_markdown(file_path, languages, blocklist)
        self.assertListEqual(blocklist, expected)