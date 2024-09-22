import unittest
import argparse
from runmd.commands import create_commons, add_run_command, add_show_command, add_list_command, add_hist_command, add_vault_command
from runmd.commands import CmdNames

class TestAddCommands(unittest.TestCase):

    def setUp(self):
        """Set up a common parser and subparsers for testing."""
        self.parser = argparse.ArgumentParser()
        self.common_parser = create_commons()
        self.subparsers = self.parser.add_subparsers(dest="command")

    # --------------------------------------------------
    # >> ADD_RUN_COMMAND
    # --------------------------------------------------

    def test_add_run_command(self):
        """Test if 'run' command is correctly added."""
        add_run_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['run', 'my_block'])
        self.assertEqual(args.command, CmdNames.RUNCMD.value)
        self.assertEqual(args.blockname, 'my_block')
        self.assertEqual(args.tag, None)
        self.assertEqual(args.env, [])

    # --------------------------------------------------
    # >> ADD_SHOW_COMMAND
    # --------------------------------------------------

    def test_add_show_command(self):
        """Test if 'show' command is correctly added."""
        add_show_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['show', 'my_block'])
        self.assertEqual(args.command, CmdNames.SHOWCMD.value)
        self.assertEqual(args.blockname, 'my_block')

    # --------------------------------------------------
    # >> ADD_LIST_COMMAND
    # --------------------------------------------------

    def test_add_list_command(self):
        """Test if 'list' command is correctly added."""
        add_list_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['list'])
        self.assertEqual(args.command, CmdNames.LISTCMD.value)
        self.assertEqual(args.tag, None)

    def test_add_list_command_with_tag(self):
        """Test if 'list' command parses the tag option."""
        add_list_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['list', '--tag', 'my_tag'])
        self.assertEqual(args.command, CmdNames.LISTCMD.value)
        self.assertEqual(args.tag, 'my_tag')

    # --------------------------------------------------
    # >> ADD_HIST_COMMAND
    # --------------------------------------------------

    def test_add_hist_command(self):
        """Test if 'hist' command is correctly added."""
        add_hist_command(self.subparsers)
        args = self.parser.parse_args(['hist'])
        self.assertEqual(args.command, CmdNames.HISTCMD.value)
        self.assertEqual(args.id, None)
        self.assertFalse(args.clear)

    def test_add_hist_command_with_clear(self):
        """Test if 'hist' command parses the --clear option."""
        add_hist_command(self.subparsers)
        args = self.parser.parse_args(['hist', '--clear'])
        self.assertEqual(args.command, CmdNames.HISTCMD.value)
        self.assertTrue(args.clear)

    # --------------------------------------------------
    # >> ADD_VAULT_COMMAND
    # --------------------------------------------------

    def test_add_vault_command(self):
        """Test if 'vault' command is correctly added."""
        add_vault_command(self.subparsers)
        args = self.parser.parse_args(['vault'])
        self.assertEqual(args.command, CmdNames.VAULTCMD.value)

    def test_add_vault_command_with_encrypt(self):
        """Test if 'vault' command parses the --encrypt option."""
        add_vault_command(self.subparsers)
        args = self.parser.parse_args(['vault', '--encrypt', 'test.md'])
        self.assertEqual(args.command, CmdNames.VAULTCMD.value)
        self.assertEqual(args.encrypt, ['test.md'])

    def test_add_vault_command_with_decrypt(self):
        """Test if 'vault' command parses the --decrypt option."""
        add_vault_command(self.subparsers)
        args = self.parser.parse_args(['vault', '--decrypt', 'test.md'])
        self.assertEqual(args.command, CmdNames.VAULTCMD.value)
        self.assertEqual(args.decrypt, ['test.md'])

    def test_add_vault_command_mutual_exclusion(self):
        """Test if 'vault' command does not allow both --encrypt and --decrypt options."""
        add_vault_command(self.subparsers)
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['vault', '--encrypt', 'test.md', '--decrypt', 'test.md'])
        

if __name__ == '__main__':
    unittest.main()
