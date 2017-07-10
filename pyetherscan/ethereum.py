"""
Library for building ethereum objects using the ETherscan API.
"""
from . import client, error


class Transaction(object):
    """
    """

    def __init__(self, address=None, hash=None):
        pass


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


class Contract(object):
    pass
