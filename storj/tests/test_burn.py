"""Burn functionality."""

import pytest
from ethereum.tester import TransactionFailed
from web3.contract import Contract


@pytest.fixture
def token_with_customer_balance(chain, team_multisig, token, customer) -> Contract:
    """Create a Crowdsale token where transfer restrictions have been lifted."""

    # Make sure customer 1 has some token balance
    token.transact({"from": team_multisig}).transfer(customer, 10000)

    return token


def test_burn(token_with_customer_balance: Contract, customer: str):
    """Burn tokens."""

    token = token_with_customer_balance
    initial_balance = token.call().balanceOf(customer)
    initial_supply = token.call().totalSupply()
    amount = 1000

    token.transact({"from": customer}).burn(amount)

    assert token.call().balanceOf(customer) == initial_balance - amount
    assert token.call().totalSupply() == initial_supply - amount

    events = token.pastEvents("Transfer").get()
    assert len(events) == 1 + 1  # plus initial transfer
    e = events[-1]
    assert e["args"]["to"] == '0x0000000000000000000000000000000000000000'
    assert e["args"]["from"] == customer
    assert e["args"]["value"] == amount

    events = token.pastEvents("Burned").get()
    assert len(events) == 1
    e = events[-1]
    assert e["args"]["burner"] == customer
    assert e["args"]["burnedAmount"] == amount
