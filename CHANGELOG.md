# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2017-07-18
### Added
- The ability to set `ETHERSCAN_API_KEY` using a configuration file (thanks
to @veox).
- Explicit tests for `pyetherscan.response` objects (vs. the previous implicit
  tests via teh `client` and `ethereum` objects).
- Contribution instructions and a virtualenv tutorial link to the README file

### Changed
- Added import statements to the packages `__init__.py` file.
- The `TransactionContainer` object enforces typing (a list must be passed).
- The `Block` and `Transaction` objects now return empty lists instead
  of `NoneType`'s
- The base `EtherscanResponse` object more explicitly validates API responses
  by checking status messages instead of the binary 1/0 status code. This
  prevents exceptions from being raised when no data is present (e.g. if
    a user has never sent a transaction).

## [0.0.2] - 2017-07-16
### Changed
- Fixed package versioning typos in the `setup.py` file.

## [0.0.1] - 2017-07-16
### Added
- PyPi badge in the `README.rst` file for python versions.
- Clarified environment variable setup in the README file.
- Added path identification support for both python 2 and 3 in the `setup.py`
  file to identify the `long_descripton` variable (previously failed for py2).

[Unreleased]: https://github.com/Marto32/pyetherscan/compare/0.1.0...HEAD
[0.1.0]: https://github.com/Marto32/pyetherscan/compare/0.0.2...0.1.0
[0.0.2]: https://github.com/Marto32/pyetherscan/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/Marto32/pyetherscan/compare/0.0.0...0.0.1
