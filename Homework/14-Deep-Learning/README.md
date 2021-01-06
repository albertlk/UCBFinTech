# LSTM Stock Predictor

In this assignment, we evaluated two different indicators with deep learning models to determine if one provided a better signal for cryptocurrencies over the other. The first indicator is the Crypto Fear and Greed Index (FNG) while the second is the closing price.

Both models were created using the same RNN architecture to ensure that the only variable being changed were the indicators themselves.

After running the model, the losses for each model for a series of different window sizes were obtained:

| Window | FNG Test Loss | Closing Test Loss |   |   |
|--------|---------------|-------------------|---|---|
| 1      | 0.0440        | 0.0010            |   |   |
| 2      | 0.0462        | 0.0013            |   |   |
| 3      | 0.0450        | 0.0025            |   |   |
| 4      | 0.0437        | 0.0025            |   |   |
| 5      | 0.0467        | 0.0031            |   |   |
| 6      | 0.0433        | 0.0020            |   |   |
| 7      | 0.0444        | 0.0021            |   |   |
| 8      | 0.0414        | 0.0020            |   |   |
| 9      | 0.4581        | 0.0023            |   |   |
| 10     | 0.4758        | 0.0027            |   |   |


The model using the closing prices performed than the FNG metric in all cases, and also tracked the actual values better over time. 

It seems that for FNG, the best window size to use is 8 days, whereas the closing price performed the best with a window size of one day. 

These differences can likely be attributed to the nature of the two metrics. Closing prices tend to be more autocorrelated the nearer they are to the day that is being predicted. FNG, on the otherhand, takes into account a larger variety of factors including surveys, social media, trends, etc. These metrics may lag more or take longer for their impact to materialize, resulting in the need for a larger window to produce better predictions.