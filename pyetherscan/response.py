"""
A module used to define API-specific response objects. All Etherscan API requests return an instance of :py:class:`EtherscanResponse`, extended to meet the endpoint's specific needs.

See :doc:`/response` for an overview.
"""
import json

from . import error


class EtherscanResponse(object):
    """
    This is the parent class for all Etherscan API responses.

    All child classes must define :py:meth:`parse_response`

    Upon initialization, the class sets the following attributes:
      - `etherscan_response`: The response json from Etherscan.
      - `response_object`: The `requests.Response <http://docs.python-requests.org/en/master/api/#requests.Response>`_ returned by the API call.
      - `status`: The Etherscan response status (independent of the `requests.Response` status).
      - `message`: The Etherscan response message.
      - Class-specific attributes are then set via the call to :py:meth:`parse_response`.

    If a `403` error is received it will raise an :py:class:`EtherscanRequestError`. This typically means the rate limit has been reached. By default, :py:meth:`get_request` and :py:meth:`post_request` will handle this and automatically retry the request.
    """

    def __init__(self, resp):
        if resp.status_code == 403:
            raise error.EtherscanRequestError(
                'Rate limit reached.'
            )

        try:
            self.etherscan_response = json.loads(resp.text)
        except AttributeError:
            raise error.EtherscanRequestError(
                'Invalid request: \n{request}'.format(
                    request=resp
                )
            )
        else:
            self.response_object = resp
            self.response_status_code = self.response_object.status_code
            self.status = self.etherscan_response.get('status')
            self.message = self.etherscan_response.get('message')
            self.parse_response()

    def parse_response(self):
        """
        The method that will parse the response object and store
        all attributes within the specific API response object.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Build a response representation like: `EtherscanResponse(resp=<Response 200>)`
        """
        return '{_class}(resp={resp})'.format(
            _class=self.__class__.__name__,
            resp=self.response_object
        )


class SingleAddressBalanceResponse(EtherscanResponse):
    """
    Represents a response object for a single address account balance call within the Etherscan `Accounts` endpoint.

    Available attributes:
      - `balance`: The balance of the address returned as a float.

    Example:

        .. code-block:: python
            In [1]: response = SingleAddressBalanceResponse(resp)

            In [2]: response.etherscan_response
            Out[2]: {
                "status":"1",
                "message":"OK",
                "result":"40807168564070000000000"
            }

            In [3]: response.balance
            Out[3]: 40807168564070000000000.0
    """

    def parse_response(self):
        """
        Parses a single balance request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":"40807168564070000000000"
                }

        """
        self.balance = float(self.etherscan_response.get('result'))


class MultiAddressBalanceResponse(EtherscanResponse):
    """
    Represents a response object for a multi address account balance call within the Etherscan `Accounts` endpoint.

    Available attributes:
      - `balances`: The balances of the addresses returned as a dict.

    Example:

        .. code-block:: python
            In [1]: response = MultiAddressBalanceResponse(resp)

            In [2]: response.etherscan_response
            Out[2]: {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "account":"0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a",
                        "balance":"40807168564070000000000"
                    }, {
                        "account":"0x63a9975ba31b0b9626b34300f7f627147df1f526",
                        "balance":"332567136222827062478"
                    }, {
                        "account":"0x198ef1ec325a96cc354c7266a038be8b5c558f67",
                        "balance":"12005264493462223951724"
                    }
                ]
            }

            In [3]: response.balances
            Out[3]: {
                '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a': 40807168564070000000000.0,
                '0x63a9975ba31b0b9626b34300f7f627147df1f526': 332567136222827062478.0,
                '0x198ef1ec325a96cc354c7266a038be8b5c558f67': 12005264493462223951724.0,
            }
    """

    def parse_response(self):
        """
        Parses a multi balance request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":[
                        {
                            "account":"0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a",
                            "balance":"40807168564070000000000"
                        }, {
                            "account":"0x63a9975ba31b0b9626b34300f7f627147df1f526",
                            "balance":"332567136222827062478"
                        }, {
                            "account":"0x198ef1ec325a96cc354c7266a038be8b5c558f67",
                            "balance":"12005264493462223951724"
                        }
                    ]
                }

        """

        address_balance_mapping_list = self.etherscan_response.get('result')
        self.balances = {
            mapping.get('account'): float(mapping.get('balance'))
            for mapping in address_balance_mapping_list
        }


class TransactionsByAddressResponse(EtherscanResponse):

    def parse_response(self):
        """
        Parses a transactions by address request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":[
                        {
                            "blockNumber":"54092",
                            "timeStamp":"1439048640",
                            "hash":"0x9c81f44c29ff0226f83...",
                            "nonce":"0",
                            "blockHash":"0xd3cabad6adab0b5...",
                            "transactionIndex":"0",
                            "from":"0x5abfec25f74cd88437631a7731906932776356f9",
                            "to":"",
                            "value":"11901464239480000000000000",
                            "gas":"2000000",
                            "gasPrice":"10000000000000",
                            "isError":"0",
                            "input":"0x6060b91f525b5ae7a03d...",
                            "contractAddress":"0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                            "cumulativeGasUsed":"1436963",
                            "gasUsed":"1436963",
                            "confirmations":"3921024"
                        }, {
                            ...
                        }
                    ]
                }

        """
        self.transactions = self.etherscan_response.get('result')


class TransactionsByHashResponse(EtherscanResponse):

    def parse_response(self):
        """
        Parses a transactions by hash request response. Example API
        response output:

            .. code-block:: python

            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "blockNumber":"1743059",
                        "timeStamp":"1466489498",
                        "from":"0x2cac6e4b11d6b58f6d3c1c9d5fe8faa89f60e5a2",
                        "to":"0x66a1c3eaf0f1ffc28d209c0763ed0ca614f3b002",
                        "value":"7106740000000000",
                        "contractAddress":"",
                        "input":"",
                        "type":"call",
                        "gas":"2300",
                        "gasUsed":"0",
                        "isError":"0",
                        "errCode":""
                    }
                ]
            }

        """
        self.transaction = self.etherscan_response.get('result')[0]


class BlocksMinedByAddressResponse(EtherscanResponse):

    def parse_response(self):
        """
        Parses a blocks mined by address request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":[
                        {
                            "blockNumber":"3462296",
                            "timeStamp":"1491118514",
                            "blockReward":"5194770940000000000"
                        }, {
                            ...
                        }
                    ]
                }

        """
        self.blocks = self.etherscan_response.get('result')


class ContractABIByAddressResponse(EtherscanResponse):

    def parse_response(self):
        """
        Parses a contract abi by address request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":[
                        {
                            'constant': True,
                            'inputs': [
                                {
                                    'name': '',
                                    'type': 'uint256'
                                }
                            ],
                            'name': 'proposals',
                            'outputs': [
                                {'name': 'recipient', 'type': 'address'},
                                {'name': 'amount', 'type': 'uint256'},
                                {'name': 'description', 'type': 'string'},
                                {'name': 'votingDeadline', 'type': 'uint256'},
                                {'name': 'open', 'type': 'bool'},
                                {'name': 'proposalPassed', 'type': 'bool'},
                                {'name': 'proposalHash', 'type': 'bytes32'},
                                {'name': 'proposalDeposit', 'type': 'uint256'},
                                {'name': 'newCurator', 'type': 'bool'},
                                {'name': 'yea', 'type': 'uint256'},
                                {'name': 'nay', 'type': 'uint256'},
                                {'name': 'creator', 'type': 'address'}
                            ],
                            'type': 'function'
                        }, {
                            ...
                        }
                    ]
                }

        """
        self.contract_abi = self.etherscan_response.get('result')


class ContractStatusResponse(EtherscanResponse):
    """
    Represents a response object for a contract status call within the Etherscan `Contracts` endpoint.

    Available attributes:
      - `contract_status`: The status of the contract returned as a json object.

    Example:

        .. code-block:: python
            In [1]: response = ContractStatusResponse(resp)

            In [2]: response.contract_status
            Out[2]: {
                "status":"1",
                "message":"OK",
                "result":{
                    "isError":"1",
                    "errDescription":"Bad jump destination"
                }
            }
    """

    def parse_response(self):
        """
        Parses a transaction status by hash request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":{
                        "isError":"1",
                        "errDescription":"Bad jump destination"
                    }
                }

        """
        self.contract_status = self.etherscan_response.get('result')


class TokenSupplyResponse(EtherscanResponse):
    """
    Represents a response object for a token supply call within the Etherscan `Tokens` endpoint.

    Available attributes:
      - `total_supply`: The total supply of the token returned as a float.

    Example:

        .. code-block:: python
            In [1]: response = TokenSupplyResponse(resp)

            In [2]: response.etherscan_response
            Out[2]: {
                "status":"1",
                "message":"OK",
                "result":"21265524714464"
            }

            In [3]: response.total_supply
            Out[3]: 21265524714464.0
    """

    def parse_response(self):
        """
        Parses a token supply by address request response. Example API
        response output:

            .. code-block:: python

                {
                    "status":"1",
                    "message":"OK",
                    "result":"21265524714464"
                }

        """
        self.total_supply = float(self.etherscan_response.get('result'))

