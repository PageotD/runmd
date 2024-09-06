import unittest
import re
from runmd.runner import detect_shebang
import configparser

class TestRunmdRunner(unittest.TestCase):

    def setUp(self):
        self.config = configparser.ConfigParser()

    # --------------------------------------------------
    # >> DETECT_SHEBANG
    # --------------------------------------------------

    def test_detect_shebang(self):
        self.config.add_section('lang.bash')
        self.config.set('lang.bash', 'aliases', 'sh, bash')
        self.config.set('lang.bash', 'command', 'bash')
        self.config.set('lang.bash', 'options', '-c')

        code = '#!/bin/bash\necho "toto"'
        result = detect_shebang(code, "lang.bash", self.config)
        self.assertEqual(result, ["/bin/bash"])

    def test_detect_shebang_none(self):
        self.config.add_section('lang.bash')
        self.config.set('lang.bash', 'aliases', 'sh, bash')
        self.config.set('lang.bash', 'command', 'bash')
        self.config.set('lang.bash', 'options', '-c')
    
        code = '#No shebang here\necho "toto"'
        result = detect_shebang(code, "lang.bash", self.config)
        self.assertEqual(result, ["bash"])