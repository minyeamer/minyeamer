-- ## 등록 월에서 12개월 후까지의 잔존율을 집계하는 쿼리 ##
WITH
	mst_intervals AS (	SELECT  1 AS interval_month UNION ALL
						SELECT  2 AS interval_month UNION ALL
						SELECT  3 AS interval_month UNION ALL
						SELECT  4 AS interval_month UNION ALL
						SELECT  5 AS interval_month UNION ALL
						SELECT  6 AS interval_month UNION ALL
						SELECT  7 AS interval_month UNION ALL
						SELECT  8 AS interval_month UNION ALL
						SELECT  9 AS interval_month UNION ALL
						SELECT 10 AS interval_month UNION ALL
						SELECT 11 AS interval_month UNION ALL
						SELECT 12 AS interval_month	),
	mst_users_with_index_month AS (	SELECT u.user_id
										 , u.register_date
										-- < SQLServer > 
										 , CAST(DATEADD(MM, i.interval_month, u.register_date) AS DATE) AS index_date
										 , SUBSTRING(u.register_date, 1, 7) AS register_month
										 , SUBSTRING(CONVERT(VARCHAR(7), DATEADD(MM, i.interval_month, u.register_date), 121), 1, 7) AS index_month
										-- < PostgreSQL >
										-- CAST(u.register_date::date + i.interval_month * '1 month'::interval AS date) AS index_date
										-- substring(u.register_date, 1, 7) AS register_month
										-- substring(CAST(u.register_date::date + i.interval_mpnth * '1 month'::interval AS text), 1, 7) AS index_month
										-- < Redshift >
										-- dateadd(month, i.interval_month, u.register_date::date) AS index_date
										-- substring(u.register_date, 1, 7) AS register_month
										-- substring(CAST(dateadd(month, i.interval_month, u.register_date::date) AS text), 1, 7) AS index_month
										-- < BigQuery >
										-- date_add(date(timestamp(u.register_date)), interval i.interval_month month) AS index_date
										-- substr(u.register_date, 1, 7) AS register_month
										-- substr(CAST(date_add(date(timestamp(u.register_date)), interval i.interval_month month) AS string), 1, 7) AS index_month
										-- < Hive, SparkSQL >
										-- add_months(u.register_date, i.interval_month) AS index_date
										-- substring(u.register_date, 1, 7) AS register_month
										-- substring(CAST(add_months(u.register_date, i.interval_month) AS string), 1, 7) AS index_month
									FROM mst_users AS u
									CROSS JOIN mst_intervals AS i	),
	action_log_in_month AS (	SELECT DISTINCT user_id
											  , SUBSTRING(stamp, 1, 7) AS action_month
											 -- < BigQuery >
											 -- substr(stamp, 1, 7) AS action_month
								FROM action_log	)
SELECT u.register_month
	 , u.index_month
	 , SUM(CASE WHEN a.action_month IS NOT NULL THEN 1 ELSE 0 END) AS users
	 , AVG(CASE WHEN a.action_month IS NOT NULL THEN 100.0 ELSE 0.0 END) AS retension_rate
FROM mst_users_with_index_month AS u
LEFT OUTER JOIN action_log_in_month AS a
	ON u.user_id = a.user_id AND u.index_month = a.action_month
GROUP BY u.register_month, u.index_month
ORDER BY u.register_month, u.index_month;