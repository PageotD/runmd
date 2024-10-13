import unittest
import dotenv
import os
from pathlib import Path
from runmd.envmanager import load_dotenv, load_process_env, update_runenv_file

class TestEnvManager(unittest.TestCase):

    def setUp(self) -> None:
        self.fake_env = {'VAR1': 'value1', 'VAR2': 'value2'}
        if os.path.exists(".runenv"):
            os.remove(".runenv")
        for key, value in self.fake_env.items():
            dotenv.set_key(".runenv", key, value)
    
    def tearDown(self) -> None:
        os.remove(".runenv")

    def test_load_dotenv(self):
        self.setUp()
        runenv = dotenv.dotenv_values(".runenv") #load_dotenv()
        self.assertIsInstance(runenv, dict)
        self.assertEqual(runenv, self.fake_env)

    def test_load_process_env(self):
        processenv = load_process_env()
        self.assertIsInstance(processenv, dict)

    def test_update_runenv_file(self):
        self.setUp()
        self.fake_env['VAR3'] = 'value3'
        runenv = load_dotenv()
        runenv['VAR3'] = 'value3'
        update_runenv_file(runenv)
        self.assertEqual(runenv, self.fake_env)