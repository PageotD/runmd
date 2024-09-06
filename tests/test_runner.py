import unittest
import re
from runmd.runner import detect_shebang

class TestRunmdRunner(unittest.TestCase):

    # --------------------------------------------------
    # >> DETECT_SHEBANG
    # --------------------------------------------------

    def test_detect_shebang(self):
        code = '#!/bin/bash\necho "toto"'
        result = detect_shebang(code)
        self.assertEqual(result, "/bin/bash")

    def test_detect_shebang_none(self):
        code = '#No shebang here\necho "toto"'
        result = detect_shebang(code)
        self.assertIsNone(result)