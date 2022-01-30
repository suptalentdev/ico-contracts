pragma solidity ^0.4.8;

import "../UpgradeableToken.sol";

/**
 * A sample token that is used as a migration testing target.
 *
 * This is not an actual token, but just a stub used in testing.
 */
contract TestMigrationTarget is StandardToken, UpgradeAgent {

  UpgradeableToken public oldToken;

  uint public originalSupply;

  function TestMigrationTarget(UpgradeableToken _oldToken) {

    oldToken = _oldToken;

    // Let's not set bad old token
    if(address(oldToken) == 0) {
      throw;
    }

    // Let's make sure we have something to migrate
    originalSupply = _oldToken.totalSupply();
    if(originalSupply == 0) {
      throw;
    }
  }

  function upgradeFrom(address _from, uint256 _value) public {
    if (msg.sender != address(oldToken)) throw; // only upgrade from oldToken

    // Mint new tokens to the migrator
    totalSupply = safeAdd(totalSupply, _value);
    balances[_from] = safeAdd(balances[_from], _value);
    Transfer(0, _from, _value);
  }

  function() public payable {
    throw;
  }

}
