# Smart Contracts with Solidity

## Associate Profit Splitter

This contract accepts Ether into the contract and divides it evenly among the asscoiate level employees. Any remaining Ether is sent back to HR

Testnet Contract Address: 0x1DADcF6b6551e3897A794f4c1c580EC83B78a4aC

### Testing the Associate Profit Splitter
To deploy the contract, enter the three addresses of the employees and click transact.

![associate_deploy](Images/Associate_Deploy.png)

To deposit into the employees' accounts, enter the amount of the deposit in the value box and click deposit.

![associate_deposit](Images/Associate_Send.png)

These are the employees' accounts prior to the deposit:

![associate_before](Images/Associate_Before.png)

These are the employees' accounts after the deposit:

![associate_after](Images/Associate_After.png)

## Tiered Profit Splitter

This contract distributes different percentages of incoming Ether to employees at different tiers. The CEO will receive 60% of the Ether, the CTO will receive 25%, and Bob will receive 15%. Any remaining Ether is sent to the CEO.

Testnet Contract Address: 0x6985Ef018A890Ea97a096c322A5DF87A0C997f28

### Testing the Tiered Profit Splitter
To deploy the contract, enter the addresses of the CEO, CTO, and Bob in the _ONE, _TWO, and _THREE fields, respectively, and click transact.

![tiered_deploy](Images/Tiered_Deploy.png)

To deposit into the employees' accounts, enter the amount of the deposit in the value box and click deposit.

![tiered_deposit](Images/Tiered_Send.png)

These are the employees' accounts prior to the deposit:

![tiered_before](Images/Tiered_Before.png)

These are the employees' accounts after the deposit:

![tiered_after](Images/Tiered_After.png)