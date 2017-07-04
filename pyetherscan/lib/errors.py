"""
Custom error definitions for Etherscan API objects.
"""

class EtherscanBaseError(Exception):
    """
    A base error class from which other Etherscan errors
    should inherit.
    """
    pass


class EtherscanInitializationError(EtherscanBaseError):
    """
    An abstract error class for Initialization related errors.
    """
    pass


class EtherscanConnectionError(EtherscanBaseError):
    """
    An abstract error class for Connection related errors.
    """
    pass


class EtherscanRequestError(EtherscanBaseError):
    """
    An abstract error class for Request related errors.
    """
    pass


class EtherscanAddressError(EtherscanBaseError):
    """
    An abstract error class for Address related errors.
    """
    pass


class EtherscanContractError(EtherscanBaseError):
    """
    An abstract error class for Contract related errors.
    """
    pass


class EtherscanTransactionError(EtherscanBaseError):
    """
    An abstract error class for Transaction related errors.
    """
    pass


class EtherscanBlockError(EtherscanBaseError):
    """
    An abstract error class for Block related errors.
    """
    pass


class EtherscanEventLogError(EtherscanBaseError):
    """
    An abstract error class for EventLog related errors.
    """
    pass


class EtherscanGethProxyError(EtherscanBaseError):
    """
    An abstract error class for GethProxy related errors.
    """
    pass


class EtherscanWebsocketError(EtherscanBaseError):
    """
    An abstract error class for Websocket related errors.
    """
    pass


class EtherscanTokenError(EtherscanBaseError):
    """
    An abstract error class for Token related errors.
    """
    pass


class EtherscanStatsError(EtherscanBaseError):
    """
    An abstract error class for Stats related errors.
    """
    pass
