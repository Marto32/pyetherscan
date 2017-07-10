import unittest
import json

from pyetherscan import response


class BaseEthereumTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def base_etherscan_response_status(self, result):
        self.assertEqual(200, result.response_status_code)
        self.assertEqual('1', result.status)
        self.assertEqual('OK', result.message)


class TestAddressObject(BaseEthereumTestCase):

    def test_retrieve_balance(self):
        pass
