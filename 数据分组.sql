SELECT COUNT(CASE WHEN IFNULL(total_money, 0) >=1000 THEN a.customer_id END ) AS '大于1000'
		,COUNT(CASE WHEN IFNULL(total_money, 0) >=800 AND IFNULL(total_money, 0)<800 THEN a.customer_id END ) AS '800~1000'
		,COUNT(CASE WHEN IFNULL(total_money, 0) <800 THEN a.customer_id END) AS '小于800'
	FROM customer_login AS a 
	LEFT JOIN
		(SELECT customer_id, COUNT(order_money) AS total_money FROM order_master GROUP BY customer_id) AS b
	ON a.customer_id=b.customer_id;
