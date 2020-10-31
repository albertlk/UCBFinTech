# Analysis of Fradulent Transactions (Part 1)

### How can you isolate (or group) the transactions of each cardholder?

Depending on your needs, you have multiple ways of doing this. If you needed the transactions of all the cardholders, but grouped by card holder, you can use "ORDER BY" so as to sort the list by card holder ID. The query for this would be: 

```SQL
CREATE VIEW trxn_by_cardholder AS
SELECT 
	t.id,
	t.date,
	t.amount,
	t.card,
	t.id_merchant,
	c.id_card_holder
FROM transactions AS t JOIN credit_card AS c ON t.card = c.card
ORDER BY c.id_card_holder;
```

Another way of doing this would be if you only needed the transactions of a specific cardholder. You can filter it so those were the only ones you saw. For example, in the below query, only the transactions of card holder 1 would be returned:

```SQL
CREATE VIEW ch_1_trxn AS
SELECT 
	t.id,
	t.date,
	t.amount,
	t.card,
	t.id_merchant,
	c.id_card_holder
FROM transactions AS t JOIN credit_card AS c ON t.card = c.card
WHERE c.id_card_holder = 1;
```
### Consider the time period 7:00 am to 9:00 am

### What are the 100 highest transactions during this time period?

To find this, you would submit the following query:

```SQL
CREATE VIEW trxn_100_7AM_9AM AS
SELECT 
	t.id,
	t.date,
	t.amount, 
	t.card, 
	t.id_merchant, 
	mc.name as "Merchant Category",
	c.id_card_holder
FROM transactions as t JOIN merchant as m ON t.id_merchant = m.id
	JOIN merchant_category as mc ON m.id_merchant_category = mc.id
	JOIN credit_card as c ON t.card = c.card
WHERE 
	date_part('hour', date) >= 7
	AND date_part('hour', date) <9
ORDER BY amount desc
LIMIT 100;
```

### Do you see any fraudulent or anomalous transactions? If you answered yes, explain why you think there might be fraudulent transactions during this time frame.

There may be a few anomolous transactions that took place during the hours of 7 am - 9am. There are a number of transactions ranging in the thousands of dollars for bars at this time. Hopefully, no one is out at this hour at bars. Though these could be valid transactions (e.g. closing out a tab from the previous night), it would be good to flag these for cardholder review.

### Some fraudsters hack a credit card by making several small payments (generally less than $2.00), which are typically ignored by cardholders. Count the transactions that are less than $2.00 per cardholder. Is there any evidence to suggest that a credit card has been hacked? Explain your rationale.

To count the number of transactions that are less than $2.00 by cardholder, we would run the following query:

```SQL
SELECT 
	c.id_card_holder,
	COUNT(t.id) as "Transaction Count"
FROM transactions as t JOIN merchant as m ON t.id_merchant = m.id
	JOIN merchant_category as mc ON m.id_merchant_category = mc.id
	JOIN credit_card as c ON t.card = c.card
WHERE 
	t.amount < 2
GROUP BY id_card_holder
ORDER BY "Transaction Count" desc;
```

From the data shown, there does not appear to be any evidence to suggest that a credit card has been hacked. There are no conspicuous outliers, with the highest count only being 26. They are relatively well distributed across the range of 3 - 26, with no one card holder having an abnormally large amount of low value transactions.

### What are the top five merchants prone to being hacked using small transactions?

To find this, we would query the top five merchants with the highest number of low value transactions (<$2):

```SQL
SELECT 
	m.id,
	m.name,
	COUNT(t.id) as "Transaction Count"
FROM transactions as t JOIN merchant as m ON t.id_merchant = m.id
	JOIN merchant_category as mc ON m.id_merchant_category = mc.id
	JOIN credit_card as c ON t.card = c.card
WHERE 
	t.amount < 2
GROUP BY 
	m.id, 
	m.name
ORDER BY "Transaction Count" desc
LIMIT 5;
```

The top five merchants are:
* Wood-Ramierz
* Hood-Phillips
* Baker Inc
* Clark and Sons
* Greene-Wood

### Visual Analysis
The visual analysis part of the project can be found in the [visual_data_analysis.ipynb](visual_data_analysis.ipynb) notebook
