in this readme file we can find all the helpful terminal commands

<!-- Creating a new network on brownie -->

>>> brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=1337

<!-- commands when trying to test a single function from test.py -->

>>> development env = brownie test -k "Function here" | testnet env = brownie test -k "function here" --network rinkeby

<!-- command to create a custom local mainnet-fork from a blockchain-->

>>> brownie networks add development mainnet-fork-alchemy cmd=ganache-cli host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/$ALCHEMY_API_ID' accounts=10 mnemonic=brownie port=8545

