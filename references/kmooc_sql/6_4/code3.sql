-- ## 매출 구성비 누계와 ABC 등급을 계산하는 쿼리 ##
WITH
	monthly_sales AS (	SELECT category
							 , SUM(price) AS amount
						FROM purchase_detail_log
						GROUP BY category	),
	sales_composition_ratio AS (	SELECT category
										 , amount
										 , 100.0 * amount / SUM(amount) OVER() AS composition_ratio
										 , 100.0 * (SELECT SUM(amount) FROM monthly_sales AS s WHERE s.amount >= m.amount) / SUM(amount) OVER() AS cumulative_ratio
									FROM monthly_sales AS m
									GROUP BY category, amount	)
SELECT *
	 , CASE WHEN cumulative_ratio BETWEEN  0 AND  75 THEN 'A'
			WHEN cumulative_ratio BETWEEN 75 AND  90 THEN 'B'
			WHEN cumulative_ratio BETWEEN 90 AND 100 THEN 'C' END AS abc_rank
FROM sales_composition_ratio
ORDER BY amount DESC;