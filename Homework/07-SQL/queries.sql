/*There are quite a few ways where you can group transactions by each card_holder. The first is by ordering transactions by id_card_holder, 
clumping the transactions of one cardholder together*/
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

/*The second way of doing this is by filtering by the specific cardholder(s) whose transactions you are interested in. In this case, we selected
the transactions of just the first card holder*/
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

/*Searching for the top 100 transactions by amount between 7 - 9 am. Added in card holder ID as wel as Merchant Category to add more details*/
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

/*Aggregating by card holder the number of transactions below $2*/
CREATE VIEW lvt_by_cardholder AS
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

/*Searching for the top 5 merchants most prone to be hacked using small transactions (e.g. those with the highest count of small transactions)*/
CREATE VIEW lvt_5_merchants AS
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