"""
Library for building ethereum objects using the ETherscan API.
"""
import datetime

from . import client, error


class Transaction(object):
    """
    Represents a generic ethereum transaction. The object is built to lazily
    parse transactions. Attributes are only evaluated when called for the
    first time.

    Public Attributes:

        - ``nonce``
        - ``contract_address``
        - ``cumulative_gas_used``
        - ``hash``
        - ``block_hash``
        - ``time_stamp``
        - ``gas``
        - ``gas_price``
        - ``value``
        - ``block_number``
        - ``block``
        - ``to``
        - ``from_``
        - ``confirmations``
        - ``input``
        - ``transaction_index``
        - ``type``
        - ``datetime_executed``
        - ``gas_used``
    """

    def __init__(self, data):
        """
        Initializes the Transaction object.

        :param data: The dictionary of data that makes up the transaction.
        :type data: dict
        """
        if not isinstance(data, dict):
            raise error.EtherscanInitializationError(
                'data must be of type dict.'
            )

        self._data = data
        self._nonce = None
        self._contract_address = None
        self._cumulative_gas_used = None
        self._hash = None
        self._block_hash = None
        self._time_stamp = None
        self._gas = None
        self._value = None
        self._block_number = None
        self._to = None
        self._confirmations = None
        self._input = None
        self._transaction_index = None
        self._from = None
        self._gas_price = None
        self._datetime_executed = None
        self._gas_used = None
        self._type = None

    def _retrieve_gas_price(self):
        self._gas_price = float(self._data.get('gasPrice'))
        return self._gas_price

    @property
    def gas_price(self):
        return self._gas_price or self._retrieve_gas_price()

    def _retrieve_from(self):
        self._from = self._data.get('from')
        return self._from

    @property
    def from_(self):
        return self._from or self._retrieve_from()

    def _retrieve_nonce(self):
        self._nonce = self._data.get('nonce')
        return self._nonce

    @property
    def nonce(self):
        return self._nonce or self._retrieve_nonce()

    def _retrieve_contract_address(self):
        self._contract_address = self._data.get('contractAddress')
        return self._contract_address

    @property
    def contract_address(self):
        return self._contract_address or self._retrieve_contract_address()

    def _retrieve_cumulative_gas_used(self):
        self._cumulative_gas_used = float(self._data.get('cumulativeGasUsed'))
        return self._cumulative_gas_used

    @property
    def cumulative_gas_used(self):
        return self._cumulative_gas_used or self._retrieve_cumulative_gas_used()

    def _retrieve_hash(self):
        self._hash = self._data.get('hash')
        return self._hash

    @property
    def hash(self):
        return self._hash or self._retrieve_hash()

    def _retrieve_block_hash(self):
        self._block_hash = self._data.get('blockHash')
        return self._block_hash

    @property
    def block_hash(self):
        return self._block_hash or self._retrieve_block_hash()

    def _retrieve_time_stamp(self):
        self._time_stamp = int(self._data.get('timeStamp'))
        return self._time_stamp

    @property
    def time_stamp(self):
        return self._time_stamp or self._retrieve_time_stamp()

    def _retrieve_gas(self):
        self._gas = float(self._data.get('gas'))
        return self._gas

    @property
    def gas(self):
        return self._gas or self._retrieve_gas()

    def _retrieve_value(self):
        self._value = float(self._data.get('value'))
        return self._value

    @property
    def value(self):
        return self._value or self._retrieve_value()

    def _retrieve_block_number(self):
        self._block_number = int(self._data.get('blockNumber'))
        return self._block_number

    @property
    def block_number(self):
        return self._block_number or self._retrieve_block_number()

    @property
    def block(self):
        return Block(self._block_number)

    def _retrieve_to(self):
        self._to = self._data.get('to')
        return self._to

    @property
    def to(self):
        return self._to or self._retrieve_to()

    def _retrieve_confirmations(self):
        self._confirmations = self._data.get('confirmations')
        return self._confirmations

    @property
    def confirmations(self):
        return self._confirmations or self._retrieve_confirmations()

    def _retrieve_input(self):
        self._input = self._data.get('input')
        return self._input

    @property
    def input(self):
        return self._input or self._retrieve_input()

    def _retrieve_transaction_index(self):
        self._transaction_index = int(self._data.get('transactionIndex'))
        return self._transaction_index

    @property
    def transaction_index(self):
        return self._transaction_index or self._retrieve_transaction_index()

    def _retrieve_gas_used(self):
        self._gas_used = float(self._data.get('gasUsed'))
        return self._gas_used

    @property
    def gas_used(self):
        return self._gas_used or self._retrieve_gas_used()

    def _retrieve_type(self):
        self._type = self._data.get('type')
        return self._type

    @property
    def type(self):
        return self._type or self._retrieve_type()

    def _convert_time_stamp(self):
        self._datetime_executed = datetime.datetime.utcfromtimestamp(
            self.time_stamp
        )
        return self._datetime_executed

    @property
    def datetime_executed(self):
        return self._datetime_executed or self._convert_time_stamp()

    def __repr__(self):
        return 'Transaction(hash={hash}, value={value}, ' \
            'datetime_executed={datetime_executed})'.format(
                hash=self.hash,
                value=self.value,
                datetime_executed=self.datetime_executed
            )


class TransactionContainer(object):
    """
    Represents a sequence of transactions (normal and internal).
    """

    def __init__(self, transaction_list):
        self.transaction_list = transaction_list

    def __iter__(self):
        for transaction in self.transaction_list:
            yield Transaction(transaction)

    def __getitem__(self, index):
        transaction_to_return = self.transaction_list[index]
        return Transaction(transaction_to_return)

    def __repr__(self):
        return 'TransactionContainer(transaction_list=<{n} transactions>)'.format(
            n=len(self.transaction_list)
        )


class Address(object):
    """
    Represents a base address.

    This uses the :py:class:`Client` object to retrieve information about, and
    construct, the ``Address``.

    Public Attributes:
        - ``address``
        - ``balance``
        - ``blocks_mined``

    Public Methods:
        - :py:method:`token_balance`

    Example Usage:

        .. code-block:: python

            In [1]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

            In [2]: ethereum_address = Address(address)

            In [3]: ethereum_address.balance
            Out[3]: 748997604382925139479303.0

            In [4]: for txn in ethereum_address.transactions:
               ...:     print(txn.value)

    """

    def __init__(self, address):
        """
        Initializes an ethereum address object.
        """
        if not isinstance(address, str):
            raise error.EtherscanInitializationError(
                "address must be a string."
            )

        self.address = address
        self.client = client.Client()
        self._transactions = None
        self._balance = None
        self._block_list = None

    def token_balance(self, contract_address):
        """
        Obtains the address's ERC-20 compliant token balance given a token
        contract address.

        :param contract_address: The address of the token contract.
        :type contract_address: str
        :returns: The balance of the token as a float.
        """
        token = self.client.get_token_balance_by_address(
            contract_address=contract_address,
            account_address=self.address
        )
        return token.balance

    def _retrieve_balance(self):
        balance_object = self.client.get_single_balance(
            self.address
        )
        self._balance = balance_object.balance
        return self._balance

    def _retrieve_transactions_for_address(self):
        normal = self.client.get_transactions_by_address(self.address)
        internal = self.client.get_transactions_by_address(
            address=self.address,
            internal=True
        )
        self._transactions = normal.transactions + internal.transactions

    @property
    def _raw_transactions(self):
        return self._transactions or self._retrieve_transactions_for_address()

    @property
    def balance(self):
        """
        The balance in ether for this address.
        """
        return self._balance or self._retrieve_balance()

    @property
    def transactions(self):
        """
        returns a :py:obj:`ethereum.TransactionContainer` object. This object
        can be treated as a sequence object containing transactions this address
        was involved in.
        """
        return TransactionContainer(self._raw_transactions)

    def _retrieve_block_list(self):
        self._block_list = self.client.get_blocks_mined_by_address(self.address)
        return self._block_list

    @property
    def blocks_mined(self):
        blocks = self._block_list or self._retrieve_block_list()
        return BlockContainer(blocks)

    def __repr__(self):
        return 'Address(address={address})'.format(
            address=self.address
        )


class BlockContainer(object):
    """
    Represents a sequence of blocks.
    """

    def __init__(self, block_list):
        self.block_list = block_list

    def __iter__(self):
        for block in self.block_list:
            block_number = int(block.get('blockNumber'))
            yield Block(block_number)

    def __getitem__(self, index):
        block_to_return = self.block_list[index]
        block_number = int(block_to_return.get('blockNumber'))
        return Block(block_number)

    def __repr__(self):
        return 'BlockContainer(block_list=<{n} blocks>)'.format(
            n=len(self.block_list)
        )


class Block(object):
    """
    Represents an ethereum block.

    This uses the :py:class:`Client` object to retrieve information about, and
    construct, the ``Block``.

    Public Attributes:
        - ``time_stamp``
        - ``block_miner``
        - ``block_reward``
        - ``uncles``
        - ``datetime_mined``
        - ``uncle_inclusion_reward``

    Example Usage:

        .. code-block:: python

            In [1]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

            In [2]: ethereum_address = Address(address)

            In [3]: ethereum_address.balance
            Out[3]: 748997604382925139479303.0

            In [4]: for txn in ethereum_address.transactions:
               ...:     print(txn.value)

    """

    def __init__(self, block_number):
        if not isinstance(block_number, (int, str)):
            raise error.EtherscanInitializationError(
                "block_number must be a string or integer."
            )

        self.block_number = block_number
        self.client = client.Client()

        self._block_reward_data = None

        self._time_stamp = None
        self._block_miner = None
        self._datetime_mined = None
        self._block_reward = None
        self._uncles = None
        self._uncle_inclusion_reward = None

    def _retrieve_block_reward_data(self):
        data = self.client.get_block_and_uncle_rewards_by_block_number(
            self.block_number
        )
        self._block_reward_data = data.rewards_data
        return self._block_reward_data

    @property
    def _raw_block_data(self):
        return self._block_reward_data or self._retrieve_block_reward_data()

    def _retrieve_time_stamp(self):
        self._time_stamp = int(self._raw_block_data.get('timeStamp'))
        return self._time_stamp

    @property
    def time_stamp(self):
        return self._time_stamp or self._retrieve_time_stamp()

    def _retrieve_block_miner(self):
        miner = str(self._raw_block_data.get('blockMiner'))
        self._block_miner = Address(miner)
        return self._block_miner

    @property
    def block_miner(self):
        return self._block_miner or self._retrieve_block_miner()

    def _convert_time_stamp(self):
        self._datetime_mined = datetime.datetime.utcfromtimestamp(
            self.time_stamp
        )
        return self._datetime_mined

    @property
    def datetime_mined(self):
        return self._datetime_mined or self._convert_time_stamp()

    def _retrieve_block_reward(self):
        self._block_reward = float(self._raw_block_data.get('blockReward'))
        return self._block_reward

    @property
    def block_reward(self):
        return self._block_reward or self._retrieve_block_reward()

    def _retrieve_uncles(self):
        uncles = self._raw_block_data.get('uncles')
        parsed_uncles = [
            {
                'miner': Address(u['miner']),
                'block_reward': float(u['blockreward'])
            } for u in uncles
        ]
        self._uncles = parsed_uncles
        return self._uncles

    @property
    def uncles(self):
        return self._uncles or self._retrieve_uncles()

    def _retrieve_uncle_inclusion_reward(self):
        self._uncle_inclusion_reward = float(
            self._raw_block_data.get('uncleInclusionReward')
        )
        return self._uncle_inclusion_reward

    @property
    def uncle_inclusion_reward(self):
        return self._uncle_inclusion_reward or \
            self._retrieve_uncle_inclusion_reward()

    def __repr__(self):
        return 'Block(block_number={block_number})'.format(
            block_number=self.block_number
        )


class Token(object):
    """
    Represents an ERC-20 compliant token.

    :param contract_address: The address of the Token contract
    :type contract_address: str
    """

    def __init__(self, contract_address):
        if not isinstance(contract_address, str):
            raise error.EtherscanInitializationError(
                "contract_address must be a string."
            )

        self.contract_address = contract_address
        self.client = client.Client()

        self._supply = None

    def _retrieve_supply(self):
        token = self.client.get_token_supply_by_address(self.contract_address)
        self._supply = token.total_supply
        return self._supply

    @property
    def supply(self):
        return self._supply or self._retrieve_supply()

    def token_balance(self, address):
        """
        The user balance of this token for a given address.

        :param address: An ethereum address.
        :type address: str
        :returns: The balance as a float.
        """
        token = self.client.get_token_balance_by_address(
            contract_address=self.contract_address,
            account_address=address
        )
        return token.balance

    def __repr__(self):
        return 'Token(contract_address={contract_address})'.format(
            contract_address=self.contract_address
        )
