import unittest
import dotenv
from pathlib import Path
from runmd.envmanager import load_dotenv, load_process_env, update_runenv, write_runenv

class TestEnvManager(unittest.TestCase):
    def test_load_dotenv(self):
        fake_env = {'VAR1': 'value1', 'VAR2': 'value2'}
        env_path = Path(".runenv")
        for key, value in fake_env.items():
            dotenv.set_key(str(env_path), key, value)
        runenv = load_dotenv()
        self.assertIsInstance(runenv, dict)
        self.assertEqual(runenv, fake_env)

    def test_load_processenv(self):
        processenv = load_process_env()
        self.assertIsInstance(processenv, dict)

    def test_update_runenv(self):
        fake_env = {'VAR1': 'value1', 'VAR2': 'value2'}
        with open(".runenv", "w") as f:
            for key, value in fake_env.items():
                dotenv.set_key(f, key, value)
        fake_updated_env = {'VAR3': 'value3', 'VAR3': 'value3'}
        runenv = load_dotenv()
        update_runenv(runenv, fake_updated_env)
        self.assertEqual(runenv, fake_env.items() + fake_updated_env.items())

    def test_write_runenv(self):
        fake_env = {'VAR1': 'value1', 'VAR2': 'value2'}
        write_runenv(fake_env)
        runenv = load_dotenv()
        self.assertEqual(runenv, fake_env)