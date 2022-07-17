//Danicoin ICO

pragma solidity ^0.4.11;

contract DaniCoin_ico 
{
    uint public total_danicoins = 1000000;
    uint public USD_danicoin_exchangerate = 1000;
    uint public total_danicoins_bought = 0;

    // mapping from the investor address to its equity in danicoins and USD
    mapping(address => uint) equity_danicoins;
    mapping(address => uint) equity_usd;

    // Check if someone can purchase danicoins
    modifier can_buy_danicoins(uint usd_amount) 
    {
        require(usd_amount * USD_danicoin_exchangerate + total_danicoins_bought <= total_danicoins );
        _;
    }

    // Get equity in danicoins of a purchaser
    function equity_in_danicoins(address purchaser) external constant returns (uint) 
    {
        return equity_danicoins(purchaser);
    }

    // Get equity in USD of a purchaser
    function equity_in_danicoins(address purchaser) external constant returns (uint) 
    {
        return equity_usd(purchaser);
    }

    // Purchasing DaniCoins
    function buy_danicoins(address purchaser, uint usd_amount) external 
    can_buy_danicoins(usd_amount)
    {
        uint danicoins_bought = usd_amount * USD_danicoin_exchangerate;
        equity_danicoins[purchaser] += danicoins_bought;
        equity_usd[purchaser] = equity_danicoins[purchaser] / USD_danicoin_exchangerate;
        total_danicoins_bought += danicoins_bought;
    }

    // Selling danicoins
    function sell_danicoins(address seller, uint danicoin_amount) external
    {
        equity_danicoins[seller] -= danicoin_amount;
        equity_usd[seller] = equity_danicoins[seller] / USD_danicoin_exchangerate;
        // Idea: Check if danicoins is not going to more than total number of danicoins
        total_danicoins_bought -= danicoin_amount;
    }
}