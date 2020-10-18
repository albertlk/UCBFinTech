# Personal Finance Planner

The first component of the notebook is to evaluate whether the member of the credit union has met the financial goal of having enough money in an emergency fund.

The inputs that are assumed are an average montly household income of $20,000 and portfolio compositions of 1.2 BTC, 5.3 ETH, 50 shares of SPY, and 200 shares of AGG. The most up to date prices for the assets were retrieved via APIs.

Afterward, a simple comparison was made to determine whether or not the amount in the portfolio was valued at more than three times the monthly income of the household. Based on this determination, a summary of the financial health is displayed to the user.

# Retirement Planning

The second component of the notebook is to forecast how the stock investments would perform at 30 year, 10 year, and 5 year milestones, based on historic stock performance. The forecast was done through Monte Carlo simulations. 

The range of possible results were given with the 95% upper and lower confidence intervals, given a prescribed initial investment. Portfolio composition was also adjusted to account for the need of riskier (and potentially greater returns) for the shorter term targets.