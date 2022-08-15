-- ## 2015년 매출에 대한 Z차트를 작성하는 쿼리 ##
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
						GROUP BY dt	),
	monthly_purchase AS (	SELECT [year]
							 , [month]
							 , [year] + '-' + [month] AS year_month
							 , SUM(purchase_amount) AS amount
						FROM daily_purchase
						GROUP BY [year], [month]	),
	calc_index AS (	SELECT [year]
						 , [month]
						 , year_month
						 , amount
						 , (SELECT SUM(CASE WHEN [year] = '2015' THEN amount END) FROM monthly_purchase AS s WHERE s.[year] = m.[year] AND s.[month] <= m.[month]) AS agg_amount
						 , (SELECT SUM(amount) FROM monthly_purchase AS s WHERE CAST(s.year_month + '-01' AS DATE)
																				BETWEEN DATEADD(MM, -11, CAST(m.year_month + '-01' AS DATE))
																				AND CAST(m.year_month + '-01' AS DATE)) AS year_avg_amount
					FROM monthly_purchase AS m	)
SELECT year_month
	 , amount
	 , agg_amount
	 , year_avg_amount
FROM calc_index
WHERE [year] = '2015'
ORDER BY year_month;