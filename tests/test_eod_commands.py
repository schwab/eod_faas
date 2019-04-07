import unittest
from eodmarket.handler import handle
import os
from unittest.mock import patch


class TestEodCommands(unittest.TestCase):
    def test_help_message_if_no_command(self):
        with patch.dict('os.environ', {'redis_host': 'redis'}):
            print(os.environ['redis_host'])  # should print out 'newvalue'
            result = handle("{}")
            self.assertIsNotNone(result)
            self.assertIn("help",result)

if __name__ == '__main__':
    unittest.main()

        
