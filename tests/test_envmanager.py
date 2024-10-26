import unittest
import dotenv
import os
from pathlib import Path
from runmd.envmanager import load_dotenv, load_process_env, update_runenv_file, merge_envs
import base64

class TestEnvManager(unittest.TestCase):

    def setUp(self) -> None:
        self.fake_env = {'VAR1': 'value1', 'VAR2': 'value2'}
        if os.path.exists(".session"):
            os.remove(".session")
        for key, value in self.fake_env.items():
            dotenv.set_key(".session", key, value)
    
    def tearDown(self) -> None:
        os.remove(".session")

    def test_load_dotenv(self):
        self.setUp()
        runenv = dotenv.dotenv_values(".session") #load_dotenv()
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
        runenv_encoded = dotenv.dotenv_values(".session")
        benv = {'VAR1': 'dmFsdWUx', 'VAR2': 'dmFsdWUy', 'VAR3': 'dmFsdWUz'}
        self.assertEqual(runenv_encoded, benv)

    def test_merge_envs(self):
        self.setUp()
        self.fake_env['VAR3'] = 'value3'
        env = {'VAR1': 'oldvalue1', 'VAR2': 'oldvalue2'}
        runenv = {'VAR1': 'dmFsdWUx', 'VAR2': 'dmFsdWUy', 'VAR3': 'dmFsdWUz'}
        merge_envs(env, runenv)
        self.assertEqual(env, self.fake_env)