import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import os
import json
import datetime
import tempfile

# Import the functions to test
from runmd.history import get_history_path, load_history, write_history, update_history, print_history, clean_command

class TestHistoryFunctions(unittest.TestCase):

    # --------------------------------------------------
    # >> UPDATE_HISTORY
    # --------------------------------------------------

    def test_update_history(self):
        history = [{"id": 1, "date": "2024-01-01T12:00:00", "root": os.getcwd(), "command": "run example.md", "status": "success"}]
        updated_history = update_history(history, 10, "run another.md", True)
        
        self.assertEqual(len(updated_history), 2)
        self.assertEqual(updated_history[-1]['id'], 2)
        self.assertEqual(updated_history[-1]['command'], "run another.md")

    # --------------------------------------------------
    # >> PRINT_HISTORY
    # --------------------------------------------------

    @patch("builtins.print")
    def test_print_history(self, mock_print):
        history = [
            {"id": 1, "date": "2024-01-01T12:00:00", "root": os.getcwd(), "command": "run example.md", "status": "success"},
            {"id": 2, "date": "2024-01-01T12:05:00", "root": os.getcwd(), "command": "run another.md", "status": "success"}
        ]
        
        print_history(history)
        mock_print.assert_any_call(f"1 2024-01-01T12:00:00 {os.getcwd()} run example.md success")
        mock_print.assert_any_call(f"2 2024-01-01T12:05:00 {os.getcwd()} run another.md success")

    # --------------------------------------------------
    # >> CLEAN_HISTORY
    # --------------------------------------------------

    def test_clean_command(self):
        command = "some/path/to/runmd/executable/runmd run someblock --file somefile"
        expected = "runmd run someblock --file somefile"

        result = clean_command(command)
        self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()
