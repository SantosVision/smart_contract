"""This scripts allow us to fund and withdraw from a smart contract """

from brownie import FundMe
from brownie.network import account
from scripts.helpful_scripts import get_access

# function to fund the smart contract
def fund():
    # gets the last contract deployed & assings it to fund_me
    fund_me = FundMe[-1]
    account = get_access()
    # gets the current entrance fee from the last contract
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is: {entrance_fee}")
    print("Funding...")
    # this function sends the funding transaction
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_access()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
