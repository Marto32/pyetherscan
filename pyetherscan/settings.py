import os

HOME_DIR = os.path.expanduser('~')
CONFIG_FILE = '.pyetherscan.ini'
PATH = os.path.join(HOME_DIR, CONFIG_FILE)
TESTING_API_KEY = 'YourApiKeyToken'

if os.path.isfile(PATH):
    try:
        from configparser import ConfigParser
    except ImportError:
        # Handle python 2.7 code
        import ConfigParser
    config = ConfigParser()
    config.read(PATH)
    ETHERSCAN_API_KEY = config['Credentials']['ETHERSCAN_API_KEY']

else:
    ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY', TESTING_API_KEY)
