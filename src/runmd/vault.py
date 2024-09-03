import argparse
import base64
import getpass
import hashlib
import json
import os
import textwrap
from pathlib import Path
from typing import Union

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TextFileVault:
    SALT_SIZE = 32
    IV_SIZE = 16
    KEY_SIZE = 32
    MAC_SIZE = 32
    CIPHER = algorithms.AES
    MODE = modes.CBC
    ENCODING = "utf-8"

    def __init__(self):
        self.password = None

    def _get_password(self):
        if self.password is None:
            password = ""
            password_confirm = "*"
            while password != password_confirm:
                password = getpass.getpass("Enter the vault password: ").encode(
                    self.ENCODING
                )
                password_confirm = getpass.getpass(
                    "Confirm the vault password: "
                ).encode(self.ENCODING)
                if password != password_confirm:
                    print("Fail password confirmation.")
            self.password = password
        return self.password

    def _derive_key(self, salt: bytes, iterations: int = 100000) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=iterations,
        )
        return kdf.derive(self._get_password())

    def _pad(self, data: bytes) -> bytes:
        padder = padding.PKCS7(self.CIPHER.block_size).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, data: bytes) -> bytes:
        unpadder = padding.PKCS7(self.CIPHER.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    def _compute_mac(self, key: bytes, ciphertext: bytes) -> bytes:
        return hashlib.sha256(key + ciphertext).digest()

    def _format_encrypted(self, data: str) -> str:
        """Format the encrypted data into 80-character lines."""
        return "\n".join(textwrap.wrap(data, width=80))

    def encrypt_file(
        self, input_path: Union[str, Path], output_path: Union[str, Path] = None
    ) -> None:
        input_path = Path(input_path)
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + ".vault")
        else:
            output_path = Path(output_path)

        with input_path.open("r", encoding=self.ENCODING) as infile:
            plaintext = infile.read().encode(self.ENCODING)

        salt = os.urandom(self.SALT_SIZE)
        iv = os.urandom(self.IV_SIZE)
        key = self._derive_key(salt)

        cipher = Cipher(self.CIPHER(key), self.MODE(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(self._pad(plaintext)) + encryptor.finalize()

        mac = self._compute_mac(key, ciphertext)

        metadata = {
            "filename": input_path.name,
            "type": input_path.suffix[1:] if input_path.suffix else "txt",
            "cipher": self.CIPHER.name,
            "mode": self.MODE.name,
            "salt_size": self.SALT_SIZE,
            "iv_size": self.IV_SIZE,
            "mac_size": self.MAC_SIZE,
        }
        metadata_json = json.dumps(metadata)

        # Combine all parts and encode to Base64
        combined = (
            metadata_json.encode(self.ENCODING) + b"\n" + salt + iv + mac + ciphertext
        )
        encoded = base64.b64encode(combined).decode(self.ENCODING)

        # Format the encoded data into 80-character lines
        formatted = self._format_encrypted(encoded)

        with output_path.open("w", encoding=self.ENCODING) as outfile:
            outfile.write(formatted)

        print(f"File encrypted and saved to {output_path}")

    def decrypt_file(
        self, input_path: Union[str, Path], output_path: Union[str, Path] = None
    ) -> None:
        input_path = Path(input_path)

        with input_path.open("r", encoding=self.ENCODING) as infile:
            # Read and join all lines to reverse the 80-character formatting
            encoded = "".join(line.strip() for line in infile)

        # Decode from Base64
        decoded = base64.b64decode(encoded)

        # Split metadata and encrypted data
        metadata_json, encrypted_data = decoded.split(b"\n", 1)
        metadata = json.loads(metadata_json.decode(self.ENCODING))

        salt = encrypted_data[: metadata["salt_size"]]
        iv = encrypted_data[
            metadata["salt_size"] : metadata["salt_size"] + metadata["iv_size"]
        ]
        mac = encrypted_data[
            metadata["salt_size"]
            + metadata["iv_size"] : metadata["salt_size"]
            + metadata["iv_size"]
            + metadata["mac_size"]
        ]
        ciphertext = encrypted_data[
            metadata["salt_size"] + metadata["iv_size"] + metadata["mac_size"] :
        ]

        key = self._derive_key(salt)

        if self._compute_mac(key, ciphertext) != mac:
            raise ValueError(
                "MAC verification failed. The file may have been tampered with."
            )

        cipher = Cipher(self.CIPHER(key), self.MODE(iv))
        decryptor = cipher.decryptor()
        plaintext = self._unpad(decryptor.update(ciphertext) + decryptor.finalize())

        if output_path is None:
            output_path = Path(metadata["filename"])
        else:
            output_path = Path(output_path)

        with output_path.open("w", encoding=self.ENCODING) as outfile:
            outfile.write(plaintext.decode(self.ENCODING))

        print(f"File decrypted and saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Text File Vault CLI")
    parser.add_argument(
        "action", choices=["encrypt", "decrypt"], help="Action to perform"
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--output", help="Path to the output file (optional)")
    args = parser.parse_args()

    vault = TextFileVault()

    if args.action == "encrypt":
        vault.encrypt_file(args.input_file, args.output)
    elif args.action == "decrypt":
        vault.decrypt_file(args.input_file, args.output)


if __name__ == "__main__":
    main()
