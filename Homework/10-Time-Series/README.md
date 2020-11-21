# Time Series and Linear Regression Findings Summary

The purpose of this analysis is to predict future movements in the value of the Japanese yen versus the U.S. dollar. Historic data was used in training and testing the data

First, taking a look at the data, the "Settle" data seems cyclic witha slight upward trend. The data does not seem to be stationary -- this should be noted for the analyses to come

## Time Series Analysis

From the time series analysis, I would buy the yen now. With the ARMA forecast, the returns for the next five days are all positive, and from the ARIMA model, we see the price being forecasted to increase as well.

From the GARCH model, the forecasts indicate that the volatility will increase over the next five days. This should be taken into account alongside the ARMA and ARIMA models as this could indicate larger swings in prices.

Further, taking a look at the model results summary, we would likely not feel too confident with using these results for trading. For both the ARMA and ARIMA models, the p values for all of the coefficients are much larger than thte standard threshold of 0.05. For the GARCH model, two of the coefficients are significant, but the third is not, so we would also want to be careful in using this model.

With such high p-values, these models are likely not very reliable to make trading decisions on.

## Linear Regression

With our linear regression model, the root-mean-squared errors for in-sample and out-of-sample predictions were calculated. For in-sample, the RMSE was 0.596, and for out-of-sample, the RMSE was 0.415. Since the out-of-sample RMSE was lower than that of in-sample, the model performed better on out-of-sample data. However, looking at the RMSE in relation to the values and magnitudes of the data, it can be concluded that neither RMSE are particularly good, and linear regression model would likely not be a reliable model to make trading decisions.