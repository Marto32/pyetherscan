import requests

from retrying import retry
from pyetherscan.util import settings
from . import errors, response


class Client(object):

    # Define etherscan API url parameters
    _base_url = 'https://api.etherscan.io/'
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

    # Define etherscan API module names
    account_module = 'account'
    contract_module = 'contract'
    transaction_module = 'transaction'
    block_module = 'block'
    event_log_module = 'logs'
    geth_proxy_module = 'proxy'
    token_module = 'stats'
    stats_module = 'stats'

    def __init__(self, apikey=settings.API_KEY, timeout=5):
        self.timeout = timeout
        self.apikey = apikey

        if not isinstance(self.apikey, str):
            raise errors.EtherscanInitializationError(
                'You must supply an API key.'
            )

        if not isinstance(self.timeout, int):
            raise errors.EtherscanInitializationError(
                'Timeout seconds must be an integer.'
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

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def get_request(self, url, response_object):
        """
        Makes a standardized GET request.
        """
        payload = self._prep_request(url)
        resp = requests.get(**payload)
        return response_object(resp)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def post_request(self, url, response_object):
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
        """
        module_uri = self._module.format(module=self.account_module)
        action_uri = self._action.format(action='balance')
        address_uri = self._address.format(address=address)
        tag_uri = self._tag.format(tag='latest')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            tag_uri + \
            self.key_uri

        return self.get_request(
            url=request_url,
            response_object=response.SingleAddressBalanceResponse
        )

    def get_multi_balance(self, addresses):
        """
        Obtains the balance for multiple addresses.
        """
        if not isinstance(addresses, list):
            raise errors.EtherscanAddressError(
                'A list must be passed to this method.'
            )

        if len(addresses) > 20:
            raise errors.EtherscanAddressError(
                'Etherscan takes a maximum of 20 addresses in a single call.'
            )

        _addresses = ','.join(addresses)
        module_uri = self._module.format(module=self.account_module)
        action_uri = self._action.format(action='balancemulti')
        address_uri = self._address.format(address=_addresses)
        tag_uri = self._tag.format(tag='latest')

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            tag_uri + \
            self.key_uri

        return self.get_request(
            url=request_url,
            response_object=response.MultiAddressBalanceResponse
        )

    def get_transactions_by_address(self, address, startblock=None,
        endblock=None, sort='asc', offset=None, page=None):
        """
        """
        module_uri = self._module.format(module=self.account_module)
        action_uri = self._action.format(action='txlist')
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
                raise errors.EtherscanTransactionError(
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

        return self.get_request(
            url=request_url,
            response_object=response.TransactionsByAddressResponse
        )

    def get_transaction_by_hash(self, hash, startblock=None,
        endblock=None, sort='asc', offset=None, page=None):
        """
        """
        module_uri = self._module.format(module=self.account_module)
        action_uri = self._action.format(action='txlistinternal')
        hash_uri = self._hash.format(hash=hash)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            hash_uri + \
            self.key_uri

        return self.get_request(
            url=request_url,
            response_object=response.TransactionsByHashResponse
        )

    def get_blocks_mined_by_address(self, address, startblock=None,
        endblock=None, sort='asc', offset=None, page=None):
        """
        """
        module_uri = self._module.format(module=self.account_module)
        action_uri = self._action.format(action='getminedblocks')
        address_uri = self._address.format(address=address)
        blocktype_uri = self._blocktype.format(blocktype='blocks')

        # If page or offset are set, _both_ must be set
        if page is not None or offset is not None:
            _both_set = page is not None and offset is not None
            if not _both_set:
                raise errors.EtherscanTransactionError(
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

        return self.get_request(
            url=request_url,
            response_object=response.BlocksMinedByAddressResponse
        )

    ########################
    # Contract API methods #
    ########################
    def get_contract_abi(self, address):
        """
        Retrieves contract abi data by address
        """
        module_uri = self._module.format(module=self.contract_module)
        action_uri = self._action.format(action='getabi')
        address_uri = self._address.format(address=address)

        request_url = self._base_url + \
            module_uri + \
            action_uri + \
            address_uri + \
            self.key_uri

        return self.get_request(
            url=request_url,
            response_object=response.ContractABIByAddressResponse
        )
