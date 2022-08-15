-- ## 카테고리별 매출과 소계를 동시에 구하는 쿼리 ##
WITH
	sub_category_amount AS (	SELECT category
									 , sub_category
									 , SUM(price) AS amount
								FROM purchase_detail_log
								GROUP BY category, sub_category	),
	category_amount AS (	SELECT category
								 , 'all' AS sub_category
								 , SUM(price) AS amount
							FROM purchase_detail_log
							GROUP BY category	),
	total_amount AS (	SELECT 'all' AS category
							 , 'all' AS sub_category
							 , SUM(price) AS amount
						FROM purchase_detail_log	)
SELECT category, sub_category, amount FROM sub_category_amount UNION ALL
SELECT category, sub_category, amount FROM category_amount UNION ALL
SELECT category, sub_category, amount FROM total_amount;