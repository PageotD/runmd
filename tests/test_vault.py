import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib
import os

from runmd.vault import TextFileVault  # Replace with the actual module name

class TestTextFileVault(unittest.TestCase):

    def setUp(self):
        self.vault = TextFileVault()

    @patch('getpass.getpass', return_value='password')
    def test_get_password(self, mock_getpass):
        password = self.vault._get_password()
        self.assertEqual(password, b'password')

    @patch('getpass.getpass', side_effect=['password', 'password'])
    def test_get_password_confirmation(self, mock_getpass):
        password = self.vault._get_password()
        self.assertEqual(password, b'password')