-- ## daily_purchase 테이블에 대해 당월 누계 매출을 집계하는 쿼리 ##
WITH
	daily_purchase AS (	SELECT dt
							-- < SQLServer > 
							 , SUBSTRING(dt, 1, 4) AS [year]
							 , SUBSTRING(dt, 6, 2) AS [month]
							 , SUBSTRING(dt, 9, 2) AS [date]
							-- < PostgreSQL, Hive, Redshift, SparkSQL >
							-- substring(dt, 1, 4) AS year
							-- substring(dt, 6, 2) AS month
							-- substring(dt, 9, 2) AS date
							-- < BigQuery >
							-- substr(dt, 1, 4) AS year
							-- substr(dt, 6, 2) AS month
							-- substr(dt, 9, 2) AS date
							 , SUM(purchase_amount) AS purchase_amount
							 , COUNT(order_id) AS orders
						FROM purchase_log
						GROUP BY dt	)
SELECT dt
	 , [year] + '-' + [month] AS year_month
	 , purchase_amount
	 , (SELECT SUM(purchase_amount) FROM daily_purchase AS s WHERE s.dt <= m.dt) AS agg_amount
FROM daily_purchase AS m
ORDER BY dt;