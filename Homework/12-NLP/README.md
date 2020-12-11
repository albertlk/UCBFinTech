# Sentiment Analysis of Cryptos

In this project, we will be analyzing news articles about two crypto currencies -- Bitcoin and Ethereum -- to get a sense of the current public sentiment around each one.

First, we ran them through a sentiment analysis. From this, we found that Ethereum generally had a more positive public sentiment around it.

It had the higher mean positive score (0.061 vs Bitcoin's 0.055), highest compound score (0.878 vs. Bitcoin's 0.765), and highest positive score (0.318 vs. Bitcoin's 0.174).

We then produced bigrams from the articles, found the top 10 words, and produced a word cloud for each of the crypto currencies:

Top 10 Words for Bitcoin:

* ('bitcoin', 12)
* ('currency', 6)
* ('cryptocurrency', 5)
* ('u', 5)
* ('representation', 5)
* ('virtual', 5)
* ('taken', 5)
* ('microsoft', 4)
* ('year', 4)
* ('november', 4)

Top 10 Words for Ethereum:

* ('bitcoin', 14)
* ('currency', 10)
* ('representation', 9)
* ('virtual', 9)
* ('seen', 7)
* ('taken', 7)
* ('new', 6)
* ('staff', 6)
* ('cryptocurrency', 5)
* ('ethereum', 5)

Word Clouds:

![Bitcoin.png](Images/Bitcoin.png)

![Ethereum.png](Images/Ethereum.png)

Finally, we used name entity recognition for both coins and visualized the tagging using displacy.