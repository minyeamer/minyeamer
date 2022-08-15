-- ## 날짜별 매출과 당월 누계 매출을 집계하는 쿼리 ##
WITH
	purchase_log_with_month AS (	SELECT dt
										-- < SQLServer > 
										 , SUBSTRING(dt, 1, 7) AS year_month
										-- < PostgreSQL, Hive, Redshift, SparkSQL >
										-- substring(dt, 1, 7) AS year_month
										-- < BigQuery >
										-- substr(dt, 1, 7) AS year_month
										 , SUM(purchase_amount) AS amount
									FROM purchase_log
									GROUP BY dt	)
SELECT dt
	 , year_month
	 , amount AS total_amount
	 , (SELECT SUM(amount) FROM purchase_log_with_month AS s WHERE s.dt <= m.dt) AS agg_amount
FROM purchase_log_with_month AS m
ORDER BY dt;