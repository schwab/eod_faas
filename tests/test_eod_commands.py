import unittest
from eodmarket.handler import handle
import os
from unittest.mock import patch


class TestEodCommands(unittest.TestCase):
    
    def test_help_message_if_no_command(self):
        with patch.dict('os.environ', {
            'redis_host': 'lepot_01',
            'redis_port':'32768'}):
            #print(os.environ['redis_host'])  # should print out 'newvalue'
            #print(os.environ['redis_port'])  # should print out 'newvalue'

            result = handle("{}")
            self.assertIsNotNone(result)
            self.assertIn("help",result)
            self.assertIn("Expected a command", result["help"])
            #print(result)

    def test_ls_markets(self):
        with patch.dict('os.environ', {
            'redis_host': 'lepot_01',
            'redis_port':'32768'}):

            result = handle('{"command":"ls:markets"}')
            self.assertIsNotNone(result)
            self.assertIn("NYSE",result)
            print(result)

    def test_ls_market_dates(self):
        with patch.dict('os.environ', {
            'redis_host': 'lepot_01',
            'redis_port':'32768'}):
            result = handle('{"command":"ls:market:dates:NYSE"}')
            print(result)

        

if __name__ == '__main__':
    unittest.main()

        
