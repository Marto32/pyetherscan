"""
Tests related to response objects.
"""
import unittest
import requests

from pyetherscan import client, response, error


class FakeResponse(requests.Response):
    """Fake instance of a Response object"""

    def __init__(self, status_code, text):
        requests.Response.__init__(self)

        self.status_code = status_code
        self._text = text

    @property
    def text(self):
        return self._text


class BaseResponseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.Client()

    def base_request_error(self, code, text):
        """Abstract testing for request errors"""
        resp = FakeResponse(code, text)
        with self.assertRaises(error.EtherscanRequestError):
            response.SingleAddressBalanceResponse(resp)


class TestInitializationResponses(BaseResponseTestCase):

    def test_rate_limit_error(self):
        self.base_request_error(403, '')

    def test_invalid_request(self):
        self.base_request_error(200, '')

    def test_bad_code_error(self):
        self.base_request_error(405, '')

    def test_data_error(self):
        text = "{\"message\":\"NOTOK\", \"result\":\"Error!\"}"
        resp = FakeResponse(200, text)

        with self.assertRaises(error.EtherscanDataError):
            response.SingleAddressBalanceResponse(resp)
