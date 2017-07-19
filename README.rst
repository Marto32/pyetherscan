.. image:: https://travis-ci.org/Marto32/pyetherscan.svg?branch=master
    :target: https://travis-ci.org/Marto32/pyetherscan

.. image:: https://coveralls.io/repos/github/Marto32/pyetherscan/badge.svg?branch=master
    :target: https://coveralls.io/github/Marto32/pyetherscan?branch=master

.. image:: https://img.shields.io/pypi/pyversions/pyetherscan.svg
    :target: https://pypi.python.org/pypi/pyetherscan

.. image:: https://img.shields.io/pypi/v/pyetherscan.svg
    :target: https://pypi.python.org/pypi/pyetherscan


pyetherscan
===========
An unofficial wrapper for the `Etherscan <https://etherscan.io>`_ API.

Installation
============
We recommend you install this library in a new `virtual environment <http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/>`_.

To install, create a new `etherscan account <https://etherscan.io>`_ and
make note of your API key. Then install the library by running:

.. code-block:: python

    pip install pyetherscan

After installation, there are two main ways to set your API key. The first
is by creating a configuration file named ``.pyetherscan.ini`` and
saving it in your home directory. The format for this file is as follows:

.. code-block:: none

    [Credentials]
    ETHERSCAN_API_KEY: YourApiKeyToken

The second is by setting the environment variable ``ETHERSCAN_API_KEY``.

If you do not use either option, the package will connect to the ropsten test
chain via the Etherscan API by default.

Usage
=====
There are two main ways to use the library. The first is via the `Client`
object to interact directly with the `Etherscan API <https://etherscan.io/apis>`_.

.. code-block:: python

    In [1]: from pyetherscan import Client

    In [2]: client = Client()

    In [3]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

    In [4]: address_balance = client.get_single_balance(address)

    In [5]: address_balance.response_status_code
    Out[5]: 200

    In [6]: address_balance.message
    Out[6]: 'OK'

    In [7]: address_balance.balance
    Out[7]: 748997604382925139479303

The second is to use ``pyetherscan`` objects which fully abstract the API. These
objects can be found in the ``pyetherscan.ethereum`` module and include:

    - ``Transaction``
    - ``Address``
    - ``Block``
    - ``Token``

For example:

.. code-block:: python

    In [1]: from pyetherscan import Address

    In [2]: address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

    In [3]: ethereum_address = Address(address)

    In [4]: ethereum_address.balance
    Out[4]: 748997604382925139479303.0

    In [4]: for txn in ethereum_address.transactions:
       ...:     print(txn.value)

Contributing
============
Fork this repository, create a branch and issue a PR.


.. image:: https://badges.gitter.im/pyetherscan/Lobby.svg
   :alt: Join the chat at https://gitter.im/pyetherscan/Lobby
   :target: https://gitter.im/pyetherscan/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
