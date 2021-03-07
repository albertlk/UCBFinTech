pragma solidity >= 0.5.0 < 0.6.0;

import "./Token.sol";
import "https://github.com/oraclize/ethereum-api/oraclizeAPI_0.5.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

contract Bank is usingOraclize {
    using SafeMath for uint;
    
    string private orcl_url = "json(http://127.0.0.1:105/SHAK_wei_price).wei";
    //string private orcl_url = "json(http://58baa9c87c8b.ngrok.io/SHAK_wei_price).wei";
    SHAKtoken private token;
    
    // Address where we'll hold all ETH
    address payable private fundwallet = msg.sender;
    uint internal rate;
    uint internal capToken;
    uint internal remainToken;
    uint internal tokenTotal;
    
    uint public contractBalance;
    
    mapping(address => uint) balances;
    
    event LogNewOraclizeQuery(string description, string url);
    event buyTokenEvent(address _from, address _to, uint _amountToken, uint _amountETH);
    event redeemTokenEvent(address _from, address _to, uint _amountToken, uint _amountETH);
    event transferTokenEvent(address _from, address _to, uint _amountToken);
    event fundWithdrawal(address _fund, uint amount);
    event totalToken(uint _amount);
    
    modifier onlyFund {
        require(msg.sender == fundwallet, "You do not have permission!");
        _;
    }
    
    constructor(uint _rate, uint _cap, address payable _fundwallet, SHAKtoken _token) public payable {
        //Assign where to hold the funds
        fundwallet = _fundwallet;
        rate = _rate;
        capToken = _cap;
        token = _token;
        remainToken = _cap;
        contractBalance = address(this).balance;
    }
    
    function getRate() public view returns (uint) { return rate; }
    function setRate(uint _rate) public onlyFund { rate = _rate; }
    
    function getCap() public view returns (uint) { return capToken; }
    function setCap(uint _cap) public onlyFund { 
        require(_cap > capToken, "Cannot reduce total token amount.");
        capToken = _cap; 
        remainToken = _cap.sub(tokenTotal);
    }
    
    function getTokenTotal() public view returns (uint) { return tokenTotal; }
    function getTokenRemain() public view returns (uint) { return remainToken; }
    
    function getcoinBalance () public view returns (uint) { return balances[msg.sender]; }
    function updateContractBalance () public { contractBalance = address(this).balance; }
    
    function setURL (string memory _url) public onlyFund {
        orcl_url = string(abi.encodePacked("json(", _url, "/SHAK_wei_price).wei"));
    }
    function getURL () public view onlyFund returns (string memory) { return orcl_url; }
    
    /*
    Function for external client to buy tokens from us
    */
    function buyToken(address payable _recv) external payable returns (bool, uint) {
        // check for cap
        require(tokenTotal < capToken, "Maximum number of token reached!");
        // updateRate - Oracalize
        updateRate();
        
        // calculate amount of tokens from msg.value
        uint token_amount;
        uint eth_tx;
        uint remainder;
        token_amount = msg.value.div(rate);
        eth_tx = msg.value.sub(remainder);
        remainder = msg.value.mod(rate);
        
        if(token_amount > remainToken){
            token_amount = remainToken;
        }
        
        // mint tokens to _recv
        SHAKtoken(address(token)).mint(_recv, token_amount);
        balances[_recv] = balances[_recv].add(token_amount);
        
        // update coinTotal
        tokenTotal = tokenTotal.add(token_amount);
        remainToken = capToken.sub(tokenTotal);
        contractBalance = address(this).balance;
        
        // return ETH from msg.sender
        (bool success, ) = msg.sender.call.value(remainder)(""); //return remainder
        require(success,"Unable to return remainder"); 
        
        // emit event
        emit buyTokenEvent(msg.sender, _recv, token_amount, eth_tx);
        emit totalToken(tokenTotal);
        // return true if succeed
        return(true, token_amount);
    }
    
    /*
    Function for external client to sell tokens back to us
    */
    function redeemToken(address payable _recv, uint amount) external payable returns (bool) {
        // check whether _source can cover buyBack
        require(balances[msg.sender] >= amount, "msg.sender doesn't have enough token.");
        // updateRate - Oracalize
        updateRate();
        // calculate amount of ETH 
        uint eth_tx;
        eth_tx = amount.mul(rate);
        
        require(eth_tx <= address(this).balance, "Unable to buy the specified amount, Please contact fund admin!");
        
        // deduct tokens
        balances[msg.sender] = balances[msg.sender].sub(amount);
        // deduct coinTotal
        tokenTotal = tokenTotal.sub(amount);
        remainToken = remainToken = capToken.sub(tokenTotal);
        
        // send ETH to _recv
        _recv.transfer(eth_tx);

        // emit event
        emit redeemTokenEvent(msg.sender, _recv, amount, eth_tx);
        emit totalToken(tokenTotal);
        // returns true if succeed
        return(true);
    }
    
    /*
    Function to transfer tokens between clients
    */
    function transferToken(address payable _recv, uint amount) public returns (bool) {
        // check whether msg.sender can cover transfer
        require(balances[msg.sender] >= amount, "msg.sender doesn't have enough token.");
        // deduct from _source
        balances[msg.sender] = balances[msg.sender].sub(amount);
        // update _recv
        balances[_recv] = balances[_recv].add(amount);
        // emit event
        emit transferTokenEvent(msg.sender, _recv, amount);
        // returns true if succeed
        return (true);
    }
    
    function withdraws(uint _amount) external payable onlyFund returns (bool, uint) {
        require(msg.value >= address(this).balance, "Unable to withdraws the specified amount.");
        (bool success, ) = fundwallet.call.value(_amount)("");
        require(success,"Unable to withdraws remainder"); 
        emit fundWithdrawal(msg.sender, _amount);
        return(true, msg.value);
    }
    
    function __callback(bytes32 myid, string memory result, bytes memory proof) public {
            //This function is executed after the result from Oracalize
           require(msg.sender == oraclize_cbAddress()); 
           rate = parseInt(result);
    }
    
    function __callback(bytes32 myid, string memory result) public {
            //This function is executed after the result from Oracalize
           require(msg.sender == oraclize_cbAddress()); 
           rate = parseInt(result);
    }
    
    function updateRate() public payable {
        string memory _url;
        _url = orcl_url;
        emit LogNewOraclizeQuery("Oraclize query was sent: ", _url);
        oraclize_query("URL", _url);
    }
    
    function() external payable {}
}

contract BankDeployer {
    address public bank_address;
    address public token_address;
    
    constructor(address payable wallet ) public {
        SHAKtoken token = new SHAKtoken();
        token_address = address(token);
        
        Bank oBank = new Bank(1, 10000000000000000000, wallet, token);
        bank_address = address(oBank);
        
        token.addMinter(bank_address);
        token.renounceMinter();
    }
}