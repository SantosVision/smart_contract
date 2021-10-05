"""This script is used to deploy the contracts"""

from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_access, deploy_mocks, LOCAL_ENV


def deploy_fund_me():
    account = get_access()

    # if we are on a persistent network like rinkeby, use the associated address.
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    # deploying mocks | the call takes 2 inputs: decilams "18" and the desire amount "200000..."
    else:
        """
        Mocks = Is used to fork and replicate a programm or software locally. in this case
        are we mocking a blockchain
        """
        deploy_mocks()
        # these functions were added to helpful_scripts.py
        # >>>  print(f"The active network is: {network.show_active()}")
        # >>>  print("Deploying Mocks...")
        # >>>  # check if the theres more than 0 mocks
        # >>>  if len(MockV3Aggregator) <= 0:
        # >>>      MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": account})

        ## gets the last aggregator address
        price_feed_address = MockV3Aggregator[-1].address
        # print("Mocks deployed!")
    # # deploying the contract and publishing it to be readable on etherscan using local network
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
