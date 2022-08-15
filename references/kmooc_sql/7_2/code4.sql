-- ## 통합 랭크를 계산하는 쿼리 ##
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
					GROUP BY user_id	),
	user_rfm_rank AS (	SELECT user_id
							 , recent_date
							 , recency
							 , frequency
							 , monetary
							 , CASE WHEN recency < 14 THEN 5
									WHEN recency < 28 THEN 4
									WHEN recency < 60 THEN 3
									WHEN recency < 90 THEN 2
									ELSE 1 END AS r
							 , CASE WHEN 20 <= frequency THEN 5
									WHEN 10 <= frequency THEN 4
									WHEN  5 <= frequency THEN 3
									WHEN  2 <= frequency THEN 2
									WHEN  1  = frequency THEN 1
									END AS f
							 , CASE WHEN 300000 <= monetary THEN 5
									WHEN 100000 <= monetary THEN 4
									WHEN  30000 <= monetary THEN 3
									WHEN   5000 <= monetary THEN 2
									ELSE 1 END AS m
						FROM user_rfm )
SELECT r + f + m AS total_rank
	 , r, f, m
	 , COUNT(user_id)
FROM user_rfm_rank
GROUP BY r, f, m
ORDER BY total_rank DESC, r DESC, f DESC, m DESC;