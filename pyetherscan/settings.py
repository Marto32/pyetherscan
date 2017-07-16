import os

TESTING_API_KEY = 'YourApiKeyToken'
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY', TESTING_API_KEY)
