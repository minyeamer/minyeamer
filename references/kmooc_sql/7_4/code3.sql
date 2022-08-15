-- ## 이전 구매일로부터의 일수를 계산하는 쿼리 ##
WITH
	purchase_log AS (	SELECT 'U001' AS user_id, '1' AS product_id, '2016-09-01' AS purchase_date UNION ALL
						SELECT 'U001' AS user_id, '2' AS product_id, '2016-09-20' AS purchase_date UNION ALL
						SELECT 'U002' AS user_id, '3' AS product_id, '2016-09-30' AS purchase_date UNION ALL
						SELECT 'U001' AS user_id, '4' AS product_id, '2016-10-01' AS purchase_date UNION ALL
						SELECT 'U002' AS user_id, '5' AS product_id, '2016-11-01' AS purchase_date	)
SELECT user_id
	 , purchase_date
	-- < SQLServer >
	 , DATEDIFF(DD, LAG(CAST(purchase_date AS DATE)) OVER(PARTITION BY user_id ORDER BY purchase_date), CAST(purchase_date AS DATE)) AS lead_time
	-- < PostgreSQL, Redshift >
	-- purchase_date::date - LAG(purchase_date::date) OVER(PARTITION BY user_id ORDER BY purchase_date) AS lead_time
	-- < BigQuery >
	-- date_diff(date(timestamp(purchase_date)), LAG(date(timestamp(purchase_date))) OVER(PARTITION BY user_id ORDER BY purchase_date), day) AS lead_time
	-- < Hive >
	-- datediff(to_date(purchase_date), LAG(to_date(purchase_date)) OVER(PARTITION BY user_id ORDER BY purchase_date)) AS lead_time
	-- < SparkSQL >
	-- datediff(to_date(purchase_date), LAG(to_date(purchase_date)) OVER(PARTITION BY user_id ORDER BY purchase_date ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING)) AS lead_time
FROM purchase_log;