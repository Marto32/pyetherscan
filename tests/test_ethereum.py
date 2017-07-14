import unittest
import datetime

from pyetherscan import response, ethereum, error


class BaseEthereumTestCase(unittest.TestCase):

    def setUp(self):
        pass


class TestAddressObject(BaseEthereumTestCase):

    def test_retrieve_balance(self):
        _address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        address = ethereum.Address(address=_address)
        self.assertEqual(address.balance, 747997604382925139479303.0)

        with self.assertRaises(error.EtherscanInitializationError):
            _bad_address = 5
            ethereum.Address(_bad_address)

    def test_transaction_property(self):
        _address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        address = ethereum.Address(address=_address)
        self.assertIsInstance(
            address.transactions,
            ethereum.TransactionContainer
        )


class TestTransactionObject(BaseEthereumTestCase):

    data = {
        "blockNumber": "80240",
        "timeStamp": "1439482422",
        "hash": "0x72f2508c262763d5ae0e51d71c0d50c881cc75c872152716b04256"
            "fe07797dcd",
        "nonce": "2",
        "blockHash": "0xb9367a1bc9094d6275ab50f4a58ce13186e35a46de68f505"
            "3487a578abf00361",
        "transactionIndex": "0",
        "from": "0xc5a96db085dda36ffbe390f455315d30d6d3dc52",
        "to": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        "value": "0",
        "gas": "377583",
        "gasPrice": "500000000000",
        "isError": "0",
        "input": "0xf00d4b5d00000000000000000000000005096a47749d8bfab0a90"
            "c1bb7a95115dbe4cea60000000000000000000000005ed8cee6b63b1c6a"
            "fce3ad7c92f4fd7e1b8fad9f",
        "contractAddress": "",
        "cumulativeGasUsed": "122207",
        "gasUsed": "122207",
        "confirmations": "3929454"
    }

    def test_initialization(self):
        with self.assertRaises(error.EtherscanInitializationError):
            ethereum.Transaction('')

    def test_transaction_attributes(self):

        transaction = ethereum.Transaction(data=self.data)

        self.assertEqual(transaction._data, self.data)
        self.assertEqual(transaction.from_, self.data.get('from'))
        self.assertEqual(transaction.hash, self.data.get('hash'))
        self.assertEqual(transaction.nonce, self.data.get('nonce'))
        self.assertEqual(transaction.block_hash, self.data.get('blockHash'))
        self.assertEqual(transaction.to, self.data.get('to'))
        self.assertEqual(transaction.value, float(self.data.get('value')))
        self.assertEqual(transaction.gas, float(self.data.get('gas')))
        self.assertEqual(transaction.input, self.data.get('input'))
        self.assertEqual(transaction.gas_used, float(self.data.get('gasUsed')))
        self.assertEqual(
            transaction.gas_price,
            float(self.data.get('gasPrice')))
        self.assertEqual(
            transaction.confirmations,
            self.data.get('confirmations'))
        self.assertEqual(
            transaction.cumulative_gas_used,
            float(self.data.get('cumulativeGasUsed')))
        self.assertEqual(
            transaction.contract_address,
            self.data.get('contractAddress'))
        self.assertEqual(
            transaction.transaction_index,
            int(self.data.get('transactionIndex')))
        self.assertEqual(
            transaction.time_stamp,
            int(self.data.get('timeStamp')))
        self.assertEqual(
            transaction.block_number,
            int(self.data.get('blockNumber')))

        datetime_ex = datetime.datetime.utcfromtimestamp(
            int(self.data.get('timeStamp'))
        )
        self.assertEqual(transaction.datetime_executed, datetime_ex)


class TestTransactionContainer(BaseEthereumTestCase):

    data = {
        "blockNumber": "80240",
        "timeStamp": "1439482422",
        "hash": "0x72f2508c262763d5ae0e51d71c0d50c881cc75c872152716b04256"
            "fe07797dcd",
        "nonce": "2",
        "blockHash": "0xb9367a1bc9094d6275ab50f4a58ce13186e35a46de68f505"
            "3487a578abf00361",
        "transactionIndex": "0",
        "from": "0xc5a96db085dda36ffbe390f455315d30d6d3dc52",
        "to": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        "value": "0",
        "gas": "377583",
        "gasPrice": "500000000000",
        "isError": "0",
        "input": "0xf00d4b5d00000000000000000000000005096a47749d8bfab0a90"
            "c1bb7a95115dbe4cea60000000000000000000000005ed8cee6b63b1c6a"
            "fce3ad7c92f4fd7e1b8fad9f",
        "contractAddress": "",
        "cumulativeGasUsed": "122207",
        "gasUsed": "122207",
        "confirmations": "3929454"
    }

    def test_retrieval(self):
        data_list = [self.data for n in range(5)]
        container = ethereum.TransactionContainer(data_list)
        self.assertEqual(
            container[0].hash,
            ethereum.Transaction(self.data).hash
        )
        for txn in container:
            self.assertEqual(
                txn.hash,
                ethereum.Transaction(self.data).hash
            )


class TestBlockObject(BaseEthereumTestCase):

    data = {
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

    uncles = [
        {
            "miner": ethereum.Address(
                "0xbcdfc35b86bedf72f0cda046a3c16829a2ef41d1"),
            "block_reward": float("3750000000000000000")
        }, {
            "miner": ethereum.Address(
                "0x0d0c9855c722ff0c78f21e43aa275a5b8ea60dce"),
            "block_reward": float("3750000000000000000")
        }
    ]

    def test_initialization(self):
        with self.assertRaises(error.EtherscanInitializationError):
            ethereum.Block(2.0)

    def test_block_attributes(self):

        block_rewards = ethereum.Block(2165403)

        self.assertEqual(
            block_rewards.time_stamp,
            int(self.data.get(
                'timeStamp')
            )
        )
        self.assertEqual(
            block_rewards.block_miner.address,
            ethereum.Address(
                self.data.get('blockMiner')
            ).address
        )
        self.assertEqual(
            block_rewards.block_reward,
            float(self.data.get(
                'blockReward')
            )
        )
        self.assertEqual(
            block_rewards.uncle_inclusion_reward,
            float(self.data.get('uncleInclusionReward'))
        )

        datetime_mined = datetime.datetime.utcfromtimestamp(
            int(self.data.get('timeStamp'))
        )
        self.assertEqual(block_rewards.datetime_mined, datetime_mined)

        # test uncles
        uncle_one_address = block_rewards.uncles[0]['miner'].address
        uncle_one_reward = block_rewards.uncles[0]['block_reward']

        expected_uncle_address = self.uncles[0]['miner'].address
        expected_uncle_reward = self.uncles[0]['block_reward']

        self.assertEqual(uncle_one_address, expected_uncle_address)
        self.assertEqual(uncle_one_reward, expected_uncle_reward)


class TestBlockContainer(BaseEthereumTestCase):

    data = {
        "blockNumber": "2691400",
        "timeStamp": "1480072029",
        "blockReward": "5086562212310617100"
    }

    def test_retrieval(self):
        data_list = [self.data for _ in range(5)]

        container = ethereum.TransactionContainer(data_list)
        expected_block_number = int(ethereum.Block(
            self.data.get('blockNumber')
        ).block_number)

        self.assertEqual(
            container[0].block_number,
            expected_block_number
        )

        for block in container:
            self.assertEqual(
                block.block_number,
                expected_block_number
            )
