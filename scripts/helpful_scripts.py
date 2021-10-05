"""This scripts are helpful function to be called in multiple modules.
this allows us to be more clean."""

from brownie import accounts, config, network, MockV3Aggregator

# the mock aggregator input
DECIMALS = 18
STARTTING_FEED = 200000000

# Local enviroment variables
LOCAL_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork-alchemy", "mainnet-fork"]

# function to get an account/address
def get_access():
    # check if the current network is in local env or forked env
    if network.show_active() in LOCAL_ENV or network.show_active() in FORKED_LOCAL_ENV:
        return accounts[0]
    else:
        account_testnet = accounts.add(config["wallets"]["metamask_rinkeby"])
        print("Rinkeby Test Network Account: ", account_testnet)
        return account_testnet


def deploy_mocks():
    print(f"The active network is: {network.show_active()}")
    print("Deploying Mocks...")
    # check if the theres less\equal than 0 mocks
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTTING_FEED, {"from": get_access()})
        # gets the last aggregator address
        # >>> price_feed_address = MockV3Aggregator[-1].address
        print("Mocks deployed!")
    # deploying the contract and publishing it to be readable on etherscan using local network
    # >>> fund_me = FundMe.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify"))
