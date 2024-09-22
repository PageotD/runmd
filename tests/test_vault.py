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
import tempfile

from runmd.vault import TextFileVault  # Replace with the actual module name

class TestTextFileVault(unittest.TestCase):

    def setUp(self):
        self.vault = TextFileVault()
        self.input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.input_file.write(b'some plain text')
        self.input_file.close()

    def tearDown(self):
        try:
            os.remove(self.input_file.name)
        except FileNotFoundError:
            pass
        
        vault_file = self.input_file.name + '.vault'
        if os.path.exists(vault_file):
            os.remove(vault_file)
    
    # --------------------------------------------------
    # >> GET_PASSWARD
    # --------------------------------------------------

    @patch('getpass.getpass', return_value='password')
    def test_get_password(self, mock_getpass):
        password = self.vault._get_password()
        self.assertEqual(password, b'password')

    @patch('getpass.getpass', side_effect=['password', 'password'])
    def test_get_password_confirmation(self, mock_getpass):
        password = self.vault._get_password()
        self.assertEqual(password, b'password')

    @patch('getpass.getpass', side_effect=['password1', 'password2', 'password', 'password'])
    def test_get_password_mismatch(self, mock_getpass):
        password = self.vault._get_password()
        self.assertEqual(password, b'password')

    # --------------------------------------------------
    # >> DERIVE_KEY
    # --------------------------------------------------

    def test_derive_key(self):
        salt = b'some_salt'
        password = b'password'
        self.vault.password = password
        key = self.vault._derive_key(salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.vault.KEY_SIZE,
            salt=salt,
            iterations=100000,
        )
        expected_key = kdf.derive(password)
        self.assertEqual(key, expected_key)

    # --------------------------------------------------
    # >> PAD
    # --------------------------------------------------

    def test_pad(self):
        data = b'some data'
        padded_data = self.vault._pad(data)
        padder = padding.PKCS7(self.vault.CIPHER.block_size).padder()
        expected_padded_data = padder.update(data) + padder.finalize()
        self.assertEqual(padded_data, expected_padded_data)

    # --------------------------------------------------
    # >> UNPAD
    # --------------------------------------------------

    def test_unpad(self):
        data = b'some data'
        padder = padding.PKCS7(self.vault.CIPHER.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        unpadded_data = self.vault._unpad(padded_data)
        self.assertEqual(unpadded_data, data)

    # --------------------------------------------------
    # >> COMPUTE_MAC
    # --------------------------------------------------

    def test_compute_mac(self):
        key = b'key'
        ciphertext = b'ciphertext'
        mac = self.vault._compute_mac(key, ciphertext)
        expected_mac = hashlib.sha256(key + ciphertext).digest()
        self.assertEqual(mac, expected_mac)