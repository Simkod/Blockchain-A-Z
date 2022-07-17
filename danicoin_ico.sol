//Danicoin ICO

pragma solidity ^0.4.11;

contract DaniCoin_ico {
    uint public total_danicoins = 1000000;
    uint public USD_danicoin_exchangerate = 1000;
    uint public total_danicoins_bought = 0;

    // mapping from the investor address to its equity in danicoins and USD
    mapping(address => uint) equity_danicoins;
    mapping(address => uint) equity_usd;

    
}