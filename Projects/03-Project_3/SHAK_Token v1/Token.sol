pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract SHAKtoken is ERC20, ERC20Detailed, ERC20Mintable {
    
    address payable bank_address;
    
    modifier onlyBank {
        require(msg.sender == bank_address, "You do not have permission!");
        _;
    }
    
    constructor() 
        ERC20Detailed("Stable Hyper Algorithmic Kryptocurrency", "SHAK", 18) public
    { }
    
}