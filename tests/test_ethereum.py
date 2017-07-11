import unittest

from pyetherscan import response, ethereum, error


class BaseEthereumTestCase(unittest.TestCase):

    def setUp(self):
        pass


class TestAddressObject(BaseEthereumTestCase):

    def test_retrieve_balance(self):
        _address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        address = ethereum.Address(address=_address)
        self.assertEqual(address.balance, 748997604382925139479303.0)

        with self.assertRaises(error.EtherscanInitializationError):
            _bad_address = 5
            ethereum.Address(_bad_address)


class TestTransactionObject(BaseEthereumTestCase):

    def test_initialization(self):
        with self.assertRaises(error.EtherscanInitializationError):
            ethereum.Transaction(address=None, hash=None)
