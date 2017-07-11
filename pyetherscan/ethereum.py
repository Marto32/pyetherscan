"""
Library for building ethereum objects using the ETherscan API.
"""
from . import client, error


class Transaction(object):
    """
    Represents a generic ethereum transaction.

    Public Attributes:

        - ``nonce``
        - ``contractAddress``
        - ``cumulativeGasUsed``
        - ``hash``
        - ``blockHash``
        - ``timeStamp``
        - ``gas``
        - ``value``
        - ``blockNumber``
        - ``to``
        - ``confirmations``
        - ``input``
    """

    def __init__(self, address=None, hash=None):
        self.address = address
        self.hash = hash

        try:
            assert address is not None or hash is not None
        except AssertionError:
            raise error.EtherscanInitializationError(
                'address or hash must be set set - both cannot be None.'
            )

        self._nonce = None
        self._contractAddress = None
        self._cumulativeGasUsed = None
        self._hash = None
        self._blockHash = None
        self._timeStamp = None
        self._gas = None
        self._value = None
        self._blockNumber = None
        self._to = None
        self._confirmations = None
        self._input = None

    def retrieve_nonce(self):
        pass

    @property
    def nonce(self):
        return self._nonce or self.retrieve_nonce()

    def retrieve_contractAddress(self):
        pass

    @property
    def contractAddress(self):
        return self._contractAddress or self.retrieve_contractAddress()

    def retrieve_cumulativeGasUsed(self):
        pass

    @property
    def cumulativeGasUsed(self):
        return self._cumulativeGasUsed or self.retrieve_cumulativeGasUsed()

    def retrieve_hash(self):
        pass

    @property
    def hash(self):
        return self._hash or self.retrieve_hash()

    def retrieve_blockHash(self):
        pass

    @property
    def blockHash(self):
        return self._blockHash or self.retrieve_blockHash()

    def retrieve_timeStamp(self):
        pass

    @property
    def timeStamp(self):
        return self._timeStamp or self.retrieve_timeStamp()

    def retrieve_gas(self):
        pass

    @property
    def gas(self):
        return self._gas or self.retrieve_gas()

    def retrieve_value(self):
        pass

    @property
    def value(self):
        return self._value or self.retrieve_value()

    def retrieve_blockNumber(self):
        pass

    @property
    def blockNumber(self):
        return self._blockNumber or self.retrieve_blockNumber()

    def retrieve_to(self):
        pass

    @property
    def to(self):
        return self._to or self.retrieve_to()

    def retrieve_confirmations(self):
        pass

    @property
    def confirmations(self):
        return self._confirmations or self.retrieve_confirmations()

    def retrieve_input(self):
        pass

    @property
    def input(self):
        return self._input or self.retrieve_input()


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

        self._balance = None

    def retrieve_balance(self):
        """
        Obtains the balance for this address using the :py:class:`Client` object.
        """
        balance_object = self.client.get_single_balance(
            self.address
        )
        self._balance = balance_object.balance
        return self._balance

    @property
    def balance(self):
        """
        The balance in ether for this address.
        """
        return self._balance or self.retrieve_balance()


class ExternalAddress(Address):
    pass


class ContractAddress(Address):
    pass


class Contract(object):
    pass
