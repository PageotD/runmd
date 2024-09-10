# import unittest
# from unittest.mock import patch, MagicMock
# import argparse
# from pathlib import Path
# import configparser
# from runmd.config import load_config
# from runmd.cli import main, execute_command

# class TestCLI(unittest.TestCase):

#     def setUp(self):
#         self.config = configparser.ConfigParser()

#     def test_cliargs_run_command(self):
#         """
#         Test that the CLI arguments for the 'run' command are parsed correctly.
#         """
#         parser = cliargs()
#         args = parser.parse_args(['run', 'my_block', '--env', 'VAR1=value1', 'VAR2=value2', '--file', 'test.md'])
        
#         # Check parsed arguments
#         self.assertEqual(args.command, 'run')
#         self.assertEqual(args.blockname, 'my_block')
#         self.assertEqual(args.env, ['VAR1=value1', 'VAR2=value2'])
#         self.assertEqual(args.file, 'test.md')

#     def test_cliargs_show_command(self):
#         """
#         Test that the CLI arguments for the 'show' command are parsed correctly.
#         """
#         parser = cliargs()
#         args = parser.parse_args(['show', 'my_block', '--file', 'test.md'])
        
#         # Check parsed arguments
#         self.assertEqual(args.command, 'show')
#         self.assertEqual(args.blockname, 'my_block')
#         self.assertEqual(args.file, 'test.md')

#     def test_cliargs_list_command(self):
#         """
#         Test that the CLI arguments for the 'list' command are parsed correctly.
#         """
#         parser = cliargs()
#         args = parser.parse_args(['list', '--tag', 'sometag', '--file', 'test.md'])
        
#         # Check parsed arguments
#         self.assertEqual(args.command, 'list')
#         self.assertEqual(args.tag, 'sometag')
#         self.assertEqual(args.file, 'test.md')

#     def test_cliargs_hist_command(self):
#         """
#         Test that the CLI arguments for the 'hist' command are parsed correctly.
#         """
#         parser = cliargs()
#         args = parser.parse_args(['hist'])
        
#         # Check parsed arguments
#         self.assertEqual(args.command, 'hist')
#         self.assertFalse(args.clear)

#     def test_cliargs_hist_command_clear(self):
#         """
#         Test that the CLI arguments for the 'hist' command are parsed correctly.
#         """
#         parser = cliargs()
#         args = parser.parse_args(['hist', '--clear'])
        
#         # Check parsed arguments
#         self.assertEqual(args.command, 'hist')
#         self.assertTrue(args.clear)


# if __name__ == '__main__':
#     unittest.main()
