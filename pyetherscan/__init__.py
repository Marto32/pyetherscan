"""
Package containing core pyetherscan functionality.
"""

from pyetherscan import client
from pyetherscan.client import Client

from pyetherscan import error
from pyetherscan.error import (
    EtherscanDataError,
    EtherscanInitializationError,
    EtherscanConnectionError,
    EtherscanRequestError,
    EtherscanAddressError,
    EtherscanContractError,
    EtherscanTransactionError,
    EtherscanBlockError,
    EtherscanEventLogError,
    EtherscanGethProxyError,
    EtherscanWebsocketError,
    EtherscanTokenError,
    EtherscanStatsError,
)

from pyetherscan import ethereum
from pyetherscan.ethereum import (
    Transaction,
    Address,
    Block,
    Token,
)

from pyetherscan import response
from pyetherscan.response import (
    SingleAddressBalanceResponse,
    MultiAddressBalanceResponse,
    TransactionsByAddressResponse,
    TransactionsByHashResponse,
    BlocksMinedByAddressResponse,
    ContractABIByAddressResponse,
    ContractStatusResponse,
    TokenSupplyResponse,
    TokenAccountBalanceResponse,
    BlockRewardsResponse,
)


__all__ = [
    'client',
    'Client',
    'error',
    'EtherscanDataError',
    'EtherscanInitializationError',
    'EtherscanConnectionError',
    'EtherscanRequestError',
    'EtherscanAddressError',
    'EtherscanContractError',
    'EtherscanTransactionError',
    'EtherscanBlockError',
    'EtherscanEventLogError',
    'EtherscanGethProxyError',
    'EtherscanWebsocketError',
    'EtherscanTokenError',
    'EtherscanStatsError',
    'ethereum',
    'Transaction',
    'Address',
    'Block',
    'Token',
    'response',
    'SingleAddressBalanceResponse',
    'MultiAddressBalanceResponse',
    'TransactionsByAddressResponse',
    'TransactionsByHashResponse',
    'BlocksMinedByAddressResponse',
    'ContractABIByAddressResponse',
    'ContractStatusResponse',
    'TokenSupplyResponse',
    'TokenAccountBalanceResponse',
    'BlockRewardsResponse',
]
