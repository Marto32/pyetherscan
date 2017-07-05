import unittest

from pyetherscan.lib import client, response


class TestAccountEndpoint(unittest.TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_get_single_balance(self):
        expected_response = {u'status': u'1', u'message': u'OK', u'result': u'748997604382925139479303'}
        address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        result = self.client.get_single_balance(address)

        self.assertEqual(response.SingleAddressBalanceResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.assertEqual(200, result.response_status_code)
        self.assertEqual('1', result.status)
        self.assertEqual('OK', result.message)
        self.assertEqual(748997604382925139479303, result.balance)


if __name__ == '__main__':
    unittest.main()
