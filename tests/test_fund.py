"""
This scripts is for testing all the functionality of the the code.
"""
from _pytest.config import exceptions
import pytest
from scripts.helpful_scripts import get_access, LOCAL_ENV
from scripts.deploy import deploy_fund_me
from brownie import network, accounts

# this function verify if the program can actually fund and withdraw
def test_fund_withdraw():
    # instantiating var
    account = get_access()
    fund_me = deploy_fund_me()
    # gets the minimun val\entrance fee
    #  added + 100 in case we need a little more to prevent error when testing
    entrance_fee = fund_me.getEntranceFee() + 100
    # sends the fund transaction
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    # waits for transaction confirmation
    tx.wait(1)
    # compare if the result of the code we intend to test is equal to the expected result.
    # in this case, we are checking if the address that send the entrance fee did actually sent the fee from that address.
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # sends the withdraw transaction
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # checks if the withdraw was successful by checking if the amount in this account is actually 0
    assert fund_me.addressToAmountFunded(account.address) == 0


# a test that only the owner can withdraw
# also test if a hacker/bad actor is trying to withdraw funds
def test_only_owner():
    # checks if the network is not in "develoment or ganache-local"
    if network.show_active() not in LOCAL_ENV:
        # if is in a test network such as rinkeby, then skip it.
        pytest.skip("only for local testing")
    # deploys the contract
    fund_me = deploy_fund_me()
    # assigns a random account for a bad actor from brownie ganache
    hacker = accounts.add()
    # uses pytest to raise an exeception for this type of error "VirtualMachineError", we want to catch that error.
    with pytest.raises(exceptions.VirtualMachineError):
        # this is the code that we want to test to see if it will catch the above error.
        fund_me.withdraw({"from": hacker})
