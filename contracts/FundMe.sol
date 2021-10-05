// SPDX-License-Identifier: MIT

// = Comments/Instructions
//>>> = Commented Codes

pragma solidity ^0.6.6;

//importing tools AggregatorV3Interface and SafeMathChainlink | linked to brownie-config.yaml
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // allaw us to do math operations using +-/
    using SafeMathChainlink for uint256;

    // maps the address to the value
    mapping(address => uint256) public addressToAmountFunded;
    // lists all the funders in this contract
    address[] public funders;
    // list the owner address
    address public owner;
    // setting a global var for the aggregator
    AggregatorV3Interface public priceFeed;

    // this constructor stablish the owner (us) of this contract instantly when deployed
    // "address _priceFeed" use to integrade the aggregatorV3Interface
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        // the sender is the owner of the address
        owner = msg.sender;
    }

    // function to create a payable event
    function fund() public payable {
        // min amount is $50 in this eg. we need to multiply by *10 n raised to the **18 so everythin has 18 decimals
        uint256 minimumUSD = 50 * 10**18;
        // the require statements works similar to the "if" statement - checks if the argument if true, if so then it continues
        // the below line says if we did not sent enought eth, we will stop here. Then revert the TX
        // "msg.value" == the amount of eth being sent by the "msg.sender" == owner of address
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        // this line updates the funds added by the funders
        addressToAmountFunded[msg.sender] += msg.value;
        // this line appends the funders to the funders empty list so we can iterate
        funders.push(msg.sender);
    }

    // interacting with the interface of the contracts
    function getVersion() public view returns (uint256) {
        // the below lines is saying that we have a interface living in this contrct address "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
        // it is commmented out because we integrated the agregator in the constructor above.
        //>>> AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //>>>     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        //>>> );
        // "priceFeed" is the variable that will call the version
        return priceFeed.version();
    }

    // the function below calls the price data using the interface from the contract
    function getPrice() public view returns (uint256) {
        // External aggregator
        //>>> AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //>>> 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        //>>> );
        // the latestRoundData will return 5 params, the "," is to ignore the params we dont need.
        // latestRoundData will return the following data:
        //>>> function latestRoundData() {
        //>>>     uint256 roundId,
        //>>>     int256 answer, <- this is the price
        //>>>     uint256 startedAt,
        //>>>     uint256 updatedAt,
        //>>>     uint80 answeredInRound };

        // in this live we are only using the "int256 answer" param
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // the "answer" data is in type "int256", but the function is calling for a type "uint256" - then use "type casting" uint256(answer)
        // the "answer" will return the price + 8 additional decimals, to convert it to "Wei" standar it has to return 18 decimals after price.
        return uint256(answer * 10000000000);
    }

    // this function wil convert the amount to USD DOLLARS
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        // this like will call the above function and assign it to "ethPrice" var
        uint256 ethPrice = getPrice();
        // this line will convert any valu they sent to USD | eg. this was the amount sent: 1000000000
        // since the value will return with 18 decimals places we devided by 18 decimals places to get the USD amount
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    // this function is to make our lives easier when dealing with math operations in the fund/withdraw events.
    function getEntranceFee() public view returns (uint256) {
        // min usd
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    // modifier (keyword) == are used to changed the behavior of a function in declarative way.
    modifier onlyOwner() {
        require(msg.sender == owner);
        // the "_" underscore is to let tell the modifier to run rest of the code after the require stattement is satisfied
        _;
    }

    // this function allows to withdraw our funds from the contract
    // onlyOwner can withdraw
    function withdraw() public payable onlyOwner {
        // "transfer" is a function that we can call on any address to send eth from 1 address to another
        // msg.sender == owner | "this" == keyword in solidity, it refes to the contract that you're currently in | "balace" == entire amount on that address\contract
        msg.sender.transfer(address(this).balance);
        // this lines resets everything to 0 when we withdraw all the balance
        // this reset every one in that mapping to 0 | source: https://www.youtube.com/watch?v=M576WGiDBdQ&t=12008s  timestamp: 3:19:00
        // we set the funderIndex to start from 0, and then the loop will finish when the funderIndex is greater or equal to the amount of funders.
        // "funderIndex++" will add an index after every sinle loop
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        // this line resets the funders array after all the fundersindex is reseted
        funders = new address[](0);
    }
}
