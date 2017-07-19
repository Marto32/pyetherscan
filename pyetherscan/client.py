"""
Library for connecting to the Etherscan API using a self contained client.
"""
import requests
import sys

from retrying import retry
from . import error, response, settings


def check_exception_for_retry(exception):
    """
    Prevent retrying if an etherscan response status is not 1.
    """
    data_error = isinstance(exception, error.EtherscanDataError)
    request_error = isinstance(exception, error.EtherscanRequestError)
    return not data_error and not request_error


RETRY_KWARGS = {
    'wait_exponential_multiplier': 1000,
    'wait_exponential_max': 10000,
    'stop_max_attempt_number': 5,
    'retry_on_exception': check_exception_for_retry,
}


class Client(object):
    """
    Represents an Etherscan API client.

    Initialized using the ETHERSCAN_API_KEY environment variable (or you may
    pass the API key as an argument).

    You can use this object to query the Etherscan database for raw data for
    each endpoint (see Public Methods below). An example is shown in the
    Example Usage section below.

    Public Attributes:
        - ``apikey``
        - ``timeout``

    Public Methods:
        - :py:meth:`get_single_balance`
        - :py:meth:`get_multi_balance`
        - :py:meth:`get_transactions_by_address`
        - :py:meth:`get_transaction_by_hash`
        - :py:meth:`get_blocks_mined_by_address`
        - :py:meth:`get_contract_abi`

    Example Usage:

        .. code-block:: python

            In [1]: client = Client()

            In [2]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

            In [3]: address_balance = client.get_single_balance(address)

            In [4]: address_balance.response_status_code
            Out[4]: 200

            In [5]: address_balance.message
            Out[5]: 'OK'

            In [6]: address_balance.balance
            Out[6]: 748997604382925139479303

    """

    # Define etherscan API url parameters
    _base_url = 'https://api.etherscan.io/'
    _test_url = 'https://ropsten.etherscan.io/'
    _module = 'api?module={module}'
    _action = '&action={action}'
    _tag = '&tag={tag}'
    _offset = '&offset={offset}'
    _page = '&page={page}'
    _sort = '&sort={sort}'
    _blocktype = '&blocktype={blocktype}'
    _key = '&apikey={key}'
    _address = '&address={address}'
    _startblock = '&startblock={startblock}'
    _endblock = '&endblock={endblock}'
    _hash = '&txhash={hash}'
    _contract_address = '&contractaddress={contract_address}'
    _blockno = '&blockno={blockno}'

    # Define etherscan API module names
    _account_module = 'account'
    _contract_module = 'contract'
    _transaction_module = 'transaction'
    _block_module = 'block'
    _event_log_module = 'logs'
    _geth_proxy_module = 'proxy'
    _token_module = 'stats'
    _stats_module = 'stats'

    def __init__(self, apikey=settings.ETHERSCAN_API_KEY, timeout=5):
        self.timeout = timeout
        self.apikey = apikey

        if sys.version_info[0] < 3:
            accepted_types = (str, unicode)
        else:
            accepted_types = str
        if not isinstance(self.apikey, accepted_types):
            raise error.EtherscanInitializationError(
                'You must supply an API key.'
            )

        # If no key is supplied, use the test network
        if self.apikey == settings.TESTING_API_KEY:
            self._base_url = self._test_url

        if not isinstance(self.timeout, (float, int)):
            raise error.EtherscanInitializationError(
                'Timeout seconds must be an integer or decimal.'
            )

        self.key_uri = self._key.format(key=self.apikey)

    def _prep_request(self, url):
        payload = {
            'url': url,
            'timeout': self.timeout,
        }
        return payload

    def __repr__(self):
        return '{_class}(apikey=<hidden>, timeout={_timeout})'.format(
            _class=self.__class__.__name__,
            _timeout=self.timeout
        )

    @retry(**RETRY_KWARGS)
    def _get_request(self, url, response_object):
        """
        Makes a standardized GET request.
        """
        payload = self._prep_request(url)
        resp = requests.get(**payload)
        return response_object(resp)

    @retry(**RETRY_KWARGS)
    def _post_request(self, url, response_object):
        """
        Makes a standardized POST request.
        """
        payload = self._prep_request(url)
        resp = requests.post(**payload)
        return response_object(resp)

    #######################
    # Address API methods #
    #######################
    def get_single_balance(self, address):
        """
        Obtains the balance for a single address.

        :param address: The ethereum address
        :type address: str
        :returns: A :py:obj:`response.SingleAddressBalanceResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

                In [3]: address_balance = client.get_single_balance(address)

                In [4]: address_balance.balance
                Out[4]: 748997604382925139479303

        """
        module_uri = self._module.format(module=self._account_module)
        action_uri = self._action.format(action='balance')
        address_uri = self._address.format(address=address)
        tag_uri = self._tag.format(tag='latest')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            tag_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.SingleAddressBalanceResponse
        )

    def get_multi_balance(self, addresses):
        """
        Obtains the balance for multiple addresses.

        :param addresses: A list of ethereum addresses, each address should
            be a string
        :type addresses: list
        :returns: A :py:obj:`response.MultiAddressBalanceResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: addresses = addresses = [
                    '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
                    '0x63a9975ba31b0b9626b34300f7f627147df1f526',
                    '0x198ef1ec325a96cc354c7266a038be8b5c558f67'
                ]

                In [3]: address_balances = client.get_multi_balance(addresses)

                In [4]: address_balances.balances
                Out[4]: {
                    u'0x198ef1ec325a96cc354c7266a038be8b5c558f67': 1.2005264493462224e+22,
                    u'0x63a9975ba31b0b9626b34300f7f627147df1f526': 3.3256713622282705e+20,
                    u'0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a': 4.080716856407e+22
                }

        """
        if not isinstance(addresses, list):
            raise error.EtherscanAddressError(
                'A list must be passed to this method.'
            )

        if len(addresses) > 20:
            raise error.EtherscanAddressError(
                'Etherscan takes a maximum of 20 addresses in a single call.'
            )

        _addresses = ','.join(addresses)
        module_uri = self._module.format(module=self._account_module)
        action_uri = self._action.format(action='balancemulti')
        address_uri = self._address.format(address=_addresses)
        tag_uri = self._tag.format(tag='latest')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            tag_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.MultiAddressBalanceResponse
        )

    def get_transactions_by_address(self, address, startblock=None,
        endblock=None, sort='asc', offset=None, page=None, internal=False):
        """
        Obtains a list of transactions for an ethereum address.

        :param address: The ethereum address
        :type address: str
        :param startblock: An optional start block to limit transactions
            (defaults to None)
        :type startblock: int
        :param endblock: An optional end block to limit transactions
            (defaults to None)
        :type endblock: int
        :param sort: Sort result set (defaults to asc)
        :type sort: str
        :param offset: The max number of results (must be used
            with ``page``)
        :type offset: int
        :param page: The page number of the result set to pull (must be used
            with ``max_results``)
        :type page: int
        :param internal: Whether or not to limit transactions to internal
            transactions (between contracts) - defaults to False
        :type internal: bool
        :returns: A :py:obj:`response.TransactionsByAddressResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

                In [3]: address_transactions = client.get_transactions_by_address(address)

                In [4]: address_transactions.transactions
                Out[4]: [
                    {
                        u'nonce': u'0',
                        u'contractAddress': u'0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae',
                        u'cumulativeGasUsed': u'1436963',
                        u'hash': u'0x9c81f44c29ff0226f835cd0a8a2f2a7eca6db52a711f8211b566fd15d3e0e8d4',
                        u'blockHash': u'0xd3cabad6adab0b52eb632c386ea194036805713682c62cb589b5abcd76de2159',
                        u'timeStamp': u'1439048640',
                        u'gas': u'2000000',
                        u'value': u'11901464239480000000000000',
                        u'blockNumber': u'54092',
                        u'to': u'',
                        u'confirmations': u'3921579',
                        u'input': u'0x606060405260....'
                    }, {
                        ...
                    }, {
                        ...
                    }
                ]

        """
        module_uri = self._module.format(module=self._account_module)
        action = 'txlistinternal' if internal else 'txlist'
        action_uri = self._action.format(action=action)
        address_uri = self._address.format(address=address)

        if startblock is None:
            startblock_uri = ''
        else:
            startblock_uri = self._startblock.format(startblock=startblock)

        if endblock is None:
            endblock_uri = ''
        else:
            endblock_uri = self._endblock.format(endblock=endblock)

        sort_uri = self._sort.format(sort=sort)

        # If page or offset are set, _both_ must be set
        if page is not None or offset is not None:
            _both_set = page is not None and offset is not None
            if not _both_set:
                raise error.EtherscanTransactionError(
                    'If using page or offset, both must be set.'
                )
            else:
                page_uri = self._page.format(page=page)
                offset_uri = self._offset.format(offset=offset)
        else:
            page_uri = self._page.format(page='')
            offset_uri = self._offset.format(offset='')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            startblock_uri + \
            endblock_uri + \
            page_uri + \
            offset_uri + \
            sort_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.TransactionsByAddressResponse
        )

    def get_transaction_by_hash(self, transaction_hash, startblock=None,
        endblock=None, sort='asc', offset=None, page=None):
        """
        Obtains transaction details for a single transaction.

        :param hash: The ethereum transaction hash
        :type hash: hash
        :returns: A :py:obj:`response.TransactionsByHashResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: hash = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'

                In [3]: transaction_details = client.get_transactions_by_hash(hash)

                In [4]: transaction_details.transaction
                Out[4]: {
                    u'contractAddress': u'',
                    u'from': u'0x2cac6e4b11d6b58f6d3c1c9d5fe8faa89f60e5a2',
                    u'timeStamp': u'1466489498',
                    u'gas': u'2300',
                    u'errCode': u'',
                    u'value': u'7106740000000000',
                    u'blockNumber': u'1743059',
                    u'to': u'0x66a1c3eaf0f1ffc28d209c0763ed0ca614f3b002',
                    u'input': u'',
                    u'type': u'call',
                    u'isError': u'0',
                    u'gasUsed': u'0'
                }

        """
        module_uri = self._module.format(module=self._account_module)
        action_uri = self._action.format(action='txlistinternal')
        transaction_hash_uri = self._hash.format(hash=transaction_hash)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            transaction_hash_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.TransactionsByHashResponse
        )

    def get_blocks_mined_by_address(self, address, startblock=None,
        endblock=None, sort='asc', offset=None, page=None):
        """
        Obtains blocks mined by a single ethereum address.

        :param address: The ethereum address
        :type address: str
        :returns: A :py:obj:`response.BlocksMinedByAddressResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: address = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'

                In [3]: blocks = client.get_blocks_mined_by_address(address)

                In [4]: blocks.blocks
                Out[4]: [
                    {
                        u'timeStamp': u'1491118514',
                        u'blockReward': u'5194770940000000000',
                        u'blockNumber': u'3462296'
                    }, {
                        u'timeStamp': u'1480072029',
                        u'blockReward': u'5086562212310617100',
                        u'blockNumber': u'2691400'
                    }, ...
                ]

        """
        module_uri = self._module.format(module=self._account_module)
        action_uri = self._action.format(action='getminedblocks')
        address_uri = self._address.format(address=address)
        blocktype_uri = self._blocktype.format(blocktype='blocks')

        # If page or offset are set, _both_ must be set
        if page is not None or offset is not None:
            _both_set = page is not None and offset is not None
            if not _both_set:
                raise error.EtherscanTransactionError(
                    'If using page or offset, both must be set.'
                )
            else:
                page_uri = self._page.format(page=page)
                offset_uri = self._offset.format(offset=offset)
        else:
            page_uri = self._page.format(page='')
            offset_uri = self._offset.format(offset='')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            blocktype_uri + \
            page_uri + \
            offset_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.BlocksMinedByAddressResponse
        )

    ########################
    # Contract API methods #
    ########################
    def get_contract_abi(self, address):
        """
        Obtains contract details by address.

        :param address: The ethereum address of the contract
        :type address: str
        :returns: A :py:obj:`response.ContractABIByAddressResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: address = '0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413'

                In [3]: contract = client.get_contract_abi(address)

                In [4]: contract.contract_abi
                Out[4]: [
                    {
                        "constant":true,
                        "inputs": [
                            {
                                "name":"",
                                "type":"uint256"
                            }
                        ],
                        "name":"proposals",
                        "outputs": [
                            {
                                "name":"recipient",
                                "type":"address"
                            }, {
                                "name":"amount",
                                "type":"uint256"
                            }, {
                                "name":"description",
                                "type":"string"
                            }, {
                                ...
                            }
                        ]
                    }

        """
        module_uri = self._module.format(module=self._contract_module)
        action_uri = self._action.format(action='getabi')
        address_uri = self._address.format(address=address)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.ContractABIByAddressResponse
        )

    ############################
    # Transactions API methods #
    ############################
    def get_contract_execution_status(self, transaction_hash):
        """
        Retrieves contract status data by tx hash. Obtains whether or not
        there was an error during contract execution.

        :param transaction_hash: The hash of the contract
        :type transaction_hash: str
        :returns: A :py:obj:`response.ContractStatusResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: hash = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'

                In [3]: contract = client.get_contract_execution_status(hash)

                In [4]: contract.contract_status
                Out[4]: {
                    u'status': u'1',
                    u'message': u'OK',
                    u'result': {
                        u'isError': u'1',
                        u'errDescription': u'Bad jump destination'
                    }
                }

        """
        module_uri = self._module.format(module=self._transaction_module)
        action_uri = self._action.format(action='getstatus')
        transaction_hash_uri = self._hash.format(hash=transaction_hash)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            transaction_hash_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.ContractStatusResponse
        )

    #####################
    # Token API methods #
    #####################
    def get_token_supply_by_address(self, address):
        """
        Retrieves total token supply for an ERC-20 compliant token given a
        contract address.

        :param address: The address of the token contract
        :type address: str
        :returns: A :py:obj:`response.TokenSupplyResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'

                In [3]: contract = client.get_token_supply_by_address(
                    contract_address
                )

                In [4]: contract.total_supply
                Out[4]: 21265524714464.0

        """
        module_uri = self._module.format(module=self._token_module)
        action_uri = self._action.format(action='tokensupply')
        contract_address_uri = self._contract_address.format(contract_address=address)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            contract_address_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.TokenSupplyResponse
        )

    def get_token_balance_by_address(self, contract_address, account_address):
        """
        Retrieves ERC-20 compliant token balance for an account given a
        contract account address.

        :param contract_address: The address of the token contract
        :type contract_address: str
        :param account_address: The address of the user account for which the
            token balance is being queried
        :type account_address: str
        :returns: A :py:obj:`response.TokenAccountBalanceResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'

                In [3]: account_address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'

                In [4]: token_balance = client.get_token_balance_by_address(
                    contract_address,
                    account_address
                )

                In [4]: token_balance.balance
                Out[4]: 135499.0

        """
        module_uri = self._module.format(module=self._account_module)
        action_uri = self._action.format(action='tokenbalance')
        contract_address_uri = self._contract_address.format(contract_address=contract_address) # noqa
        address_uri = self._address.format(address=account_address)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            contract_address_uri + \
            address_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.TokenAccountBalanceResponse
        )

    #####################
    # Block API methods #
    #####################
    def get_block_and_uncle_rewards_by_block_number(self, block_number):
        """
        Retrieves block and uncle rewards by block number.

        :param block_number: The address of the token contract
        :type block_number: str or int
        :returns: A :py:obj:`response.TokenAccountBalanceResponse` instance

        Example Usage:

            .. code-block:: python

                In [1]: client = Client()

                In [2]: block_number = 2165403

                In [3]: block_data = client.get_block_and_uncle_rewards_by_block_number(
                    block_number
                )

                In [4]: block_data.rewards_data
                Out[4]: {
                    "blockNumber": "2165403",
                    "timeStamp": "1472533979",
                    "blockMiner": "0x13a06d3dfe21e0db5c016c03ea7d2509f7f8d1e3",
                    "blockReward": "5314181600000000000",
                    "uncles": [
                        {
                            "miner": "0xbcdfc35b86bedf72f0cda046a3c16829a2ef41d1",
                            "unclePosition": "0",
                            "blockreward": "3750000000000000000"
                        }, {
                            "miner": "0x0d0c9855c722ff0c78f21e43aa275a5b8ea60dce",
                            "unclePosition": "1",
                            "blockreward": "3750000000000000000"
                        }
                    ],
                    "uncleInclusionReward": "312500000000000000"
                }

        """
        module_uri = self._module.format(module=self._block_module)
        action_uri = self._action.format(action='getblockreward')
        blockno_uri = self._blockno.format(blockno=block_number)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            blockno_uri + \
            self.key_uri

        return self._get_request(
            url=request_url,
            response_object=response.BlockRewardsResponse
        )
