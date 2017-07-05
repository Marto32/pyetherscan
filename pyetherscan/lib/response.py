import json

from . import errors


class EtherscanResponse(object):

    def __init__(self, resp):
        """
        """
        if resp.status_code == 403:
            raise errors.EtherscanRequestError(
                'Rate limit reached.'
            )

        try:
            self.etherscan_response = json.loads(resp.text)
        except AttributeError:
            raise EtherscanRequestError(
                'Invalid request: \n{request}'.format(
                    request=resp
                )
            )
        else:
            self.response_object = resp
            self.response_status_code = self.response_object.status_code
            self._parse_response()

    def _parse_response(self):
        """
        The method that will parse the response object and store
        all attributes within the specific API response object.
        """
        raise NotImplementedError

    def __repr__(self):
        attribute_list = [
            '{k}={v}'.format(k=_key, v=_val) for _key, _val in self.__dict__.items()
        ]

        return '{_class}(resp={resp}) -> Attributes:\n{attrs}'.format(
            _class=self.__class__.__name__,
            resp=self.response_object,
            attrs='\n'.join(attribute_list)
        )


class SingleAddressBalanceResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a single balance request response. Example API
        response output:
            ```
            {
                "status":"1",
                "message":"OK",
                "result":"40807168564070000000000"
            }
            ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')
        self.balance = int(self.etherscan_response.get('result'))


class MultiAddressBalanceResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a multi balance request response. Example API
        response output:
            ```
            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "account":"0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a",
                        "balance":"40807168564070000000000"
                    }, {
                        "account":"0x63a9975ba31b0b9626b34300f7f627147df1f526",
                        "balance":"332567136222827062478"
                    }, {
                        "account":"0x198ef1ec325a96cc354c7266a038be8b5c558f67",
                        "balance":"12005264493462223951724"
                    }
                ]
            }
            ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')

        address_balance_mapping_list = self.etherscan_response.get('result')
        self.balances = {
            mapping.get('account'): mapping.get('balance')
            for mapping in address_balance_mapping_list
        }


class TransactionsByAddressResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a transactions by address request response. Example API
        response output:
            ```
            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "blockNumber":"54092",
                        "timeStamp":"1439048640",
                        "hash":"0x9c81f44c29ff0226f83...",
                        "nonce":"0",
                        "blockHash":"0xd3cabad6adab0b5...",
                        "transactionIndex":"0",
                        "from":"0x5abfec25f74cd88437631a7731906932776356f9",
                        "to":"",
                        "value":"11901464239480000000000000",
                        "gas":"2000000",
                        "gasPrice":"10000000000000",
                        "isError":"0",
                        "input":"0x6060b91f525b5ae7a03d...",
                        "contractAddress":"0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
                        "cumulativeGasUsed":"1436963",
                        "gasUsed":"1436963",
                        "confirmations":"3921024"
                    }, {
                        ...
                    }
                ]
            }
            ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')
        self.transactions = self.etherscan_response.get('result')


class TransactionsByHashResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a transactions by hash request response. Example API
        response output:
            ```
            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "blockNumber":"1743059",
                        "timeStamp":"1466489498",
                        "from":"0x2cac6e4b11d6b58f6d3c1c9d5fe8faa89f60e5a2",
                        "to":"0x66a1c3eaf0f1ffc28d209c0763ed0ca614f3b002",
                        "value":"7106740000000000",
                        "contractAddress":"",
                        "input":"",
                        "type":"call",
                        "gas":"2300",
                        "gasUsed":"0",
                        "isError":"0",
                        "errCode":""
                    }
                ]
            }
            ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')
        self.transaction = self.etherscan_response.get('result')[0]


class BlocksMinedByAddressResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a blocks mined by address request response. Example API
        response output:
            ```
            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "blockNumber":"3462296",
                        "timeStamp":"1491118514",
                        "blockReward":"5194770940000000000"
                    }, {
                        ...
                    }
                ]
            }
            ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')
        self.blocks = self.etherscan_response.get('result')


class ContractABIByAddressResponse(EtherscanResponse):

    def _parse_response(self):
        """
        Parses a contract abi by address request response. Example API
        response output:
        ```
        {
            "status":"1",
            "message":"OK",
            "result":[
                {
                    'constant': True,
                    'inputs': [
                        {
                            'name': '',
                            'type': 'uint256'
                        }
                    ],
                    'name': 'proposals',
                    'outputs': [
                        {'name': 'recipient', 'type': 'address'},
                        {'name': 'amount', 'type': 'uint256'},
                        {'name': 'description', 'type': 'string'},
                        {'name': 'votingDeadline', 'type': 'uint256'},
                        {'name': 'open', 'type': 'bool'},
                        {'name': 'proposalPassed', 'type': 'bool'},
                        {'name': 'proposalHash', 'type': 'bytes32'},
                        {'name': 'proposalDeposit', 'type': 'uint256'},
                        {'name': 'newCurator', 'type': 'bool'},
                        {'name': 'yea', 'type': 'uint256'},
                        {'name': 'nay', 'type': 'uint256'},
                        {'name': 'creator', 'type': 'address'}
                    ],
                    'type': 'function'
                }, {
                    ...
                }
            ]
        }
        ```
        """
        self.status = self.etherscan_response.get('status')
        self.message = self.etherscan_response.get('message')
        self.contract_abi = self.etherscan_response.get('result')
