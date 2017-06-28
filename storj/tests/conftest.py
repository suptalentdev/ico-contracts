"""Fixtures used in testing."""

import pytest
from web3.contract import Contract


@pytest.fixture
def token_name() -> str:
    return "Unit test token"


@pytest.fixture
def token_symbol() -> str:
    return "TEST"


@pytest.fixture
def initial_supply() -> str:
    return 500000000


@pytest.fixture
def customer(accounts) -> str:
    """Get a customer address."""
    return accounts[1]


@pytest.fixture
def customer_2(accounts) -> str:
    """Get another customer address."""
    return accounts[2]


@pytest.fixture
def beneficiary(accounts) -> str:
    """The team control address."""
    return accounts[3]


@pytest.fixture
def team_multisig(accounts) -> str:
    """The team multisig address."""
    return accounts[4]


@pytest.fixture
def token_owner(team_multisig) -> str:
    """Upgrade master for the token."""
    return team_multisig


@pytest.fixture
def malicious_address(accounts) -> str:
    """Somebody who tries to perform activities they are not allowed to."""
    return accounts[5]


@pytest.fixture
def empty_address(accounts):
    """This account never holds anything."""
    return accounts[6]


@pytest.fixture
def allowed_party(accounts):
    """Gets ERC-20 allowance."""
    return accounts[7]


@pytest.fixture
def token(chain, team_multisig, token_name, token_symbol, initial_supply) -> Contract:
    """Create the token contract."""

    args = [team_multisig, token_name, token_symbol, initial_supply, 0]

    tx = {
        "from": team_multisig
    }

    contract, hash = chain.provider.deploy_contract('CentrallyIssuedToken', deploy_args=args, deploy_transaction=tx)
    return contract
