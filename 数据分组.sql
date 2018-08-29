SELECT COUNT(CASE WHEN IFNULL(total_money, 0) >=1000 THEN a.customer_id END ) AS '大于1000'
		,COUNT(CASE WHEN IFNULL(total_money, 0) >=800 AND IFNULL(total_money, 0)<800 THEN a.customer_id END ) AS '800~1000'
		,COUNT(CASE WHEN IFNULL(total_money, 0) <800 THEN a.customer_id END) AS '小于800'
	FROM customer AS a 
	LEFT JOIN
		(SELECT cust_id, COUNT(oder_money) AS toal_money FROM ordr_mster GROUP BY cust_id) AS b
	ON a.cust_id=b.cust_id;
