-- ## 사용자별로 RFM을 집계하는 쿼리 ##
WITH
	purchase_log AS (	SELECT user_id
							 , amount
							-- < SQLServer, PostgreSQL, Hive, Redshift, SparkSQL >
							 , SUBSTRING(stamp, 1, 10) AS dt
							-- < PostgreSQL, Hive, BigQuery, SparkSQL >
							-- SUBSTR(stamp, 1, 10) AS dt
						FROM action_log
						WHERE action = 'purchase'	),
	user_rfm AS (	SELECT user_id
						 , MAX(dt) AS recent_date
						-- < SQLServer >
						 , DATEDIFF(DD, CONVERT(DATETIME, MAX(dt)), GETDATE()) AS recency
						-- < PostgreSQL, Redshift >
						-- CURRENT_DATE - MAX(dt::date) AS receny
						-- < BigQuery >
						-- date_diff(CURRENT_DATE, date(timestamp(MAX(dt))), day) AS recency
						-- < Hive, SparkSQL >
						-- datediff(CURRENT_DATE(), to_date(MAX(dt))) AS recency
						 , COUNT(dt) AS frequency
						 , SUM(amount) AS monetary
					FROM purchase_log
					GROUP BY user_id	)
SELECT *
FROM user_rfm;