import unittest
import json

from pyetherscan import client, response


class BaseClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.Client()

    def base_etherscan_response_status(self, result):
        self.assertEqual(200, result.response_status_code)
        self.assertEqual('1', result.status)
        self.assertEqual('OK', result.message)

class TestAccountEndpoint(BaseClientTestCase):

    def test_get_single_balance(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': u'748997604382925139479303'
        }
        address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        result = self.client.get_single_balance(address)

        self.assertEqual(response.SingleAddressBalanceResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.assertEqual(748997604382925139479303.0, result.balance)
        self.base_etherscan_response_status(result)

    def test_get_multi_balance(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': [
                {
                    u'account': u'0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
                    u'balance': u'40807168564070000000000'
                }, {
                    u'account': u'0x63a9975ba31b0b9626b34300f7f627147df1f526',
                    u'balance': u'332567136222827062478'
                }, {
                    u'account': u'0x198ef1ec325a96cc354c7266a038be8b5c558f67',
                    u'balance': u'12005264493462223951724'
                }
            ]
        }
        addresses = [
            '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
            '0x63a9975ba31b0b9626b34300f7f627147df1f526',
            '0x198ef1ec325a96cc354c7266a038be8b5c558f67'
        ]
        result = self.client.get_multi_balance(addresses)

        self.assertEqual(response.MultiAddressBalanceResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)

        balances = {
            u'0x198ef1ec325a96cc354c7266a038be8b5c558f67': 1.2005264493462224e+22,
            u'0x63a9975ba31b0b9626b34300f7f627147df1f526': 3.3256713622282705e+20,
            u'0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a': 4.080716856407e+22
        }
        self.assertEqual(balances, result.balances)
        self.base_etherscan_response_status(result)

    def test_get_transactions_by_address(self):
        address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
        result = self.client.get_transactions_by_address(address)

        self.assertEqual(response.TransactionsByAddressResponse, type(result))
        # self.assertEqual(expected_response_result_sorted, etherscan_response_sorted)
        self.base_etherscan_response_status(result)

    def test_get_transaction_by_hash(self):
        transaction = {
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
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': [transaction]
        }
        hash = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        result = self.client.get_transaction_by_hash(hash)

        self.assertEqual(response.TransactionsByHashResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.assertEqual(transaction, result.transaction)
        self.base_etherscan_response_status(result)

    def test_get_blocks_mined_by_address(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': [
                {
                    u'timeStamp': u'1491118514',
                    u'blockReward': u'5194770940000000000',
                    u'blockNumber': u'3462296'
                }
            ]
        }
        address = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'
        result = self.client.get_blocks_mined_by_address(address)

        self.assertEqual(response.BlocksMinedByAddressResponse, type(result))

        eth_response_result = result.etherscan_response.get('result')[0]
        expected_response_result = expected_response.get('result')[0]
        self.assertEqual(eth_response_result, expected_response_result)
        self.assertEqual(
            expected_response.get('status'),
            result.etherscan_response.get('status')
        )
        self.assertEqual(
            expected_response.get('message'),
            result.etherscan_response.get('message')
        )
        self.base_etherscan_response_status(result)


class TestContractEndpoint(BaseClientTestCase):

    def test_get_contract_abi(self):
        contract_abi = {
                "constant":True,
                "inputs":[
                    {
                        "name":"",
                        "type":"uint256"
                    }
                ],
                "name":"proposals",
                "outputs":[
                    {
                        "name":"recipient",
                        "type":"address"
                    },{
                        "name":"amount",
                        "type":"uint256"
                    },{
                        "name":"description",
                        "type":"string"
                    },{
                        "name":"votingDeadline",
                        "type":"uint256"
                    },{
                        "name":"open",
                        "type":"bool"
                    },{
                        "name":"proposalPassed",
                        "type":"bool"
                    },{
                        "name":"proposalHash",
                        "type":"bytes32"
                    },{
                        "name":"proposalDeposit",
                        "type":"uint256"
                    },{
                        "name":"newCurator",
                        "type":"bool"
                    },{
                        "name":"yea",
                        "type":"uint256"
                    },{
                        "name":"nay",
                        "type":"uint256"
                    },{
                        "name":"creator",
                        "type":"address"
                    }
                ],
                "type":"function"
            }

        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': contract_abi
        }

        address = '0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413'
        result = self.client.get_contract_abi(address)

        self.assertEqual(response.ContractABIByAddressResponse, type(result))

        truncated_response = json.loads(
            result.etherscan_response.get('result'))[0]
        exp_truncated = expected_response.get('result')

        self.assertEqual(
            exp_truncated,
            truncated_response
        )

        self.assertEqual(
            expected_response.get('status'),
            result.etherscan_response.get('status')
        )

        self.assertEqual(
            expected_response.get('message'),
            result.etherscan_response.get('message')
        )

        self.base_etherscan_response_status(result)


class TestTransactionsEndpoint(BaseClientTestCase):

    def test_get_contract_execution_status(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': {
                u'isError': u'1',
                u'errDescription':
                u'Bad jump destination'
            }
        }
        hash = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'
        result = self.client.get_contract_execution_status(hash)

        self.assertEqual(response.ContractStatusResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.base_etherscan_response_status(result)


class TestTokenEndpoint(BaseClientTestCase):

    def test_get_token_supply_by_address(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': u'21265524714464'
        }
        address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
        result = self.client.get_token_supply_by_address(address)

        self.assertEqual(response.TokenSupplyResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.assertEqual(21265524714464.0, result.total_supply)
        self.base_etherscan_response_status(result)

    def test_get_token_balance_by_address(self):
        expected_response = {
            u'status': u'1',
            u'message': u'OK',
            u'result': u'135499'
        }

        contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
        account_address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
        result = self.client.get_token_balance_by_address(
            contract_address,
            account_address
        )

        self.assertEqual(response.TokenAccountBalanceResponse, type(result))
        self.assertEqual(expected_response, result.etherscan_response)
        self.assertEqual(135499.0, result.balance)
        self.base_etherscan_response_status(result)


if __name__ == '__main__':
    unittest.main()
