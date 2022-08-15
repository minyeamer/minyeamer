-- ## 날짜별 매출을 일시 테이블로 만드는 쿼리 ##
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
SELECT *
FROM daily_purchase
ORDER BY dt;