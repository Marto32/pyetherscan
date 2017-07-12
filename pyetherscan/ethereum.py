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

    def _retrieve_gas_price(self):
        return float(self._data.get('gasPrice'))

    @property
    def gas_price(self):
        return self._gas_price or self._retrieve_gas_price()

    def _retrieve_from(self):
        return self._data.get('from')

    @property
    def from_(self):
        return self._from or self._retrieve_from()

    def _retrieve_nonce(self):
        return self._data.get('nonce')

    @property
    def nonce(self):
        return self._nonce or self._retrieve_nonce()

    def _retrieve_contract_address(self):
        return self._data.get('contractAddress')

    @property
    def contract_address(self):
        return self._contract_address or self._retrieve_contract_address()

    def _retrieve_cumulative_gas_used(self):
        return float(self._data.get('cumulativeGasUsed'))

    @property
    def cumulative_gas_used(self):
        return self._cumulative_gas_used or self._retrieve_cumulative_gas_used()

    def _retrieve_hash(self):
        return self._data.get('hash')

    @property
    def hash(self):
        return self._hash or self._retrieve_hash()

    def _retrieve_block_hash(self):
        return self._data.get('blockHash')

    @property
    def block_hash(self):
        return self._block_hash or self._retrieve_block_hash()

    def _retrieve_time_stamp(self):
        return int(self._data.get('timeStamp'))

    @property
    def time_stamp(self):
        return self._time_stamp or self._retrieve_time_stamp()

    def _retrieve_gas(self):
        return float(self._data.get('gas'))

    @property
    def gas(self):
        return self._gas or self._retrieve_gas()

    def _retrieve_value(self):
        return float(self._data.get('value'))

    @property
    def value(self):
        return self._value or self._retrieve_value()

    def _retrieve_block_number(self):
        return int(self._data.get('blockNumber'))

    @property
    def block_number(self):
        return self._block_number or self._retrieve_block_number()

    def _retrieve_to(self):
        return self._data.get('to')

    @property
    def to(self):
        return self._to or self._retrieve_to()

    def _retrieve_confirmations(self):
        return self._data.get('confirmations')

    @property
    def confirmations(self):
        return self._confirmations or self._retrieve_confirmations()

    def _retrieve_input(self):
        return self._data.get('input')

    @property
    def input(self):
        return self._input or self._retrieve_input()

    def _retrieve_transaction_index(self):
        return int(self._data.get('transactionIndex'))

    @property
    def transaction_index(self):
        return self._transaction_index or self._retrieve_transaction_index()

    def _retrieve_gas_used(self):
        return float(self._data.get('gasUsed'))

    @property
    def gas_used(self):
        return self._gas_used or self._retrieve_gas_used()

    def _retrieve_type(self):
        return self._data.get('type')

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


class TransactionContainer(object):
    """
    Represents a sequence of transactions (normal and internal).
    """

    def __init__(self, transaction_list):
        """
        Initializes a transaction container object
        """
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

    Public Methods:
        - :py:meth:`retrieve_balance`

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
        # TODO Add block functionality to address

    def retrieve_balance(self):
        """
        Obtains the balance for this address using the :py:class:`Client` object.
        """
        balance_object = self.client.get_single_balance(
            self.address
        )
        self._balance = balance_object.balance
        return self._balance

    def retrieve_transactions_for_address(self):
        """
        Obtains all transactions this address was involved in.
        :returns: list of transaction dict objects
        """
        normal = self.client.get_transactions_by_address(self.address)
        internal = self.client.get_transactions_by_address(
            address=self.address,
            internal=True
        )
        self._transactions = normal.transactions + internal.transactions

    @property
    def raw_transactions(self):
        return self._transactions or self.retrieve_transactions_for_address()

    @property
    def balance(self):
        """
        The balance in ether for this address.
        """
        return self._balance or self.retrieve_balance()

    @property
    def transactions(self):
        """
        returns a :py:obj:`ethereum.TransactionContainer` object. This object
        can be treated as a sequence object containing transactions this address
        was involved in.
        """
        return TransactionContainer(self.raw_transactions)


class Contract(object):  # TODO
    """Represents a contract."""
    pass


class Block(object):  # TODO
    """Represents a block."""
    pass


class Token(object):  # TODO
    """Represents an ERC-20 compliant token."""
    pass
