-- ## 월별 매출과 작대비를 계산하는 쿼리 ##
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
SELECT [month]
	 , SUM(CASE [year] WHEN '2014' THEN purchase_amount END) AS amount_2014
	 , SUM(CASE [year] WHEN '2015' THEN purchase_amount END) AS amount_2015
	 , 100.0
	   * SUM(CASE [year] WHEN '2015' THEN purchase_amount END)
	   / SUM(CASE [year] WHEN '2014' THEN purchase_amount END) AS rate
FROM daily_purchase
GROUP BY [month]
ORDER BY [month];