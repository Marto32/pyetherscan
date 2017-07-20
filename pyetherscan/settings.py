import os
import sys

HOME_DIR = os.path.expanduser('~')
CONFIG_FILE = '.pyetherscan.ini'
PATH = os.path.join(HOME_DIR, CONFIG_FILE)
TESTING_API_KEY = 'YourApiKeyToken'


def parse_configs(python_version, config_object):
    """
    A helper function to parse configuration files in
    python 2 and 3.
    """
    if python_version < 3:
        return config_object.get('Credentials', 'ETHERSCAN_API_KEY')
    else:
        return config_object['Credentials']['ETHERSCAN_API_KEY']


if os.path.isfile(PATH):
    try:
        from configparser import ConfigParser
    except ImportError:
        # Handle python 2.7 code
        from ConfigParser import ConfigParser
    config = ConfigParser()
    config.read(PATH)
    ETHERSCAN_API_KEY = parse_configs(sys.version_info[0], config)

else:
    ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY', TESTING_API_KEY)
