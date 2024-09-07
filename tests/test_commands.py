import unittest
import argparse
from runmd.commands import create_commons, add_run_command, add_show_command, add_list_command, add_hist_command
from runmd.commands import RUNCMD, SHOWCMD, LISTCMD, HISTCMD

class TestAddCommands(unittest.TestCase):

    def setUp(self):
        """Set up a common parser and subparsers for testing."""
        self.parser = argparse.ArgumentParser()
        self.common_parser = create_commons()
        self.subparsers = self.parser.add_subparsers(dest="command")

    def test_add_run_command(self):
        """Test if 'run' command is correctly added."""
        add_run_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['run', 'my_block'])
        self.assertEqual(args.command, RUNCMD)
        self.assertEqual(args.blockname, 'my_block')
        self.assertEqual(args.tag, None)
        self.assertEqual(args.env, [])

    def test_add_show_command(self):
        """Test if 'show' command is correctly added."""
        add_show_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['show', 'my_block'])
        self.assertEqual(args.command, SHOWCMD)
        self.assertEqual(args.blockname, 'my_block')

    def test_add_list_command(self):
        """Test if 'list' command is correctly added."""
        add_list_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['list'])
        self.assertEqual(args.command, LISTCMD)
        self.assertEqual(args.tag, None)

    def test_add_list_command_with_tag(self):
        """Test if 'list' command parses the tag option."""
        add_list_command(self.subparsers, self.common_parser)
        args = self.parser.parse_args(['list', '--tag', 'my_tag'])
        self.assertEqual(args.command, LISTCMD)
        self.assertEqual(args.tag, 'my_tag')

    def test_add_hist_command(self):
        """Test if 'hist' command is correctly added."""
        add_hist_command(self.subparsers)
        args = self.parser.parse_args(['hist'])
        self.assertEqual(args.command, HISTCMD)
        self.assertEqual(args.id, None)
        self.assertFalse(args.clear)

    def test_add_hist_command_with_clear(self):
        """Test if 'hist' command parses the --clear option."""
        add_hist_command(self.subparsers)
        args = self.parser.parse_args(['hist', '--clear'])
        self.assertEqual(args.command, HISTCMD)
        self.assertTrue(args.clear)

if __name__ == '__main__':
    unittest.main()
