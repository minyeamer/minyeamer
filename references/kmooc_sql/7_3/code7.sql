-- ## 정착률을 계산하는 쿼리 ##
WITH
	repeat_interval AS (	SELECT '07 day retention' AS index_name,  1 AS interval_begin_date,  7 AS interval_end_date UNION ALL
							SELECT '14 day retention' AS index_name,  8 AS interval_begin_date, 14 AS interval_end_date UNION ALL
							SELECT '21 day retention' AS index_name, 15 AS interval_begin_date, 21 AS interval_end_date UNION ALL
							SELECT '28 day retention' AS index_name, 22 AS interval_begin_date, 28 AS interval_end_date	),
	action_log_with_index_date AS (	SELECT u.user_id
										 , u.register_date
										 , CAST(a.stamp AS DATE) AS action_date
										 , MAX(CAST(a.stamp AS DATE)) OVER() AS latest_date
										-- < BigQuery >
										-- date(timestamp(a.stamp)) AS action_date
										-- MAX(date(timestamp(a.stamp))) OVER() AS latest_date
										, r.index_name
										-- < SQLServer > 
										 , CAST(DATEADD(DD, r.interval_begin_date, u.register_date) AS DATE) AS index_begin_date
										 , CAST(DATEADD(DD, r.interval_end_date, u.register_date) AS DATE) AS index_end_date
										-- < PostgreSQL >
										-- CAST(u.register_date::date + '1 day'::interval * r.interval_begin_date AS date) AS index_begin_date
										-- CAST(u.register_date::date + '1 day'::interval * r.interval_end_date AS date) AS index_end_date
										-- < Redshift >
										-- dateadd(day, r.interval_begin_date, u.register_date::date) AS index_begin_date
										-- dateadd(day, r.interval_end_date, u.register_date::date) AS index_end_date
										-- < BigQuery >
										-- date_add(CAST(u.register_date AS date), interval r.interval_begin_date day) AS index_begin_date
										-- date_add(CAST(u.register_date AS date), interval r.interval_end_date day) AS index_end_date
										-- < Hive, SparkSQL >
										-- date_add(CAST(u.register_date AS date), r.interval_begin_date) AS index_begin_date
										-- date_add(CAST(u.register_date AS date), r.interval_end_date) AS index_end_date
									FROM mst_users AS u
									LEFT OUTER JOIN action_log AS a
										ON u.user_id = a.user_id
									CROSS JOIN repeat_interval AS r	),
	user_action_flag AS (	SELECT user_id
								 , register_date
								 , index_name
								 , SIGN(SUM(CASE WHEN index_end_date <= latest_date THEN
												CASE WHEN action_date BETWEEN index_begin_date AND index_end_date THEN 1 ELSE 0 END
											END)) AS index_date_action
							FROM action_log_with_index_date
							GROUP BY user_id, register_date, index_name, index_begin_date, index_end_date	)
SELECT register_date
	 , index_name
	 , AVG(100.0 * index_date_action) AS index_rate
FROM user_action_flag
GROUP BY register_date, index_name
ORDER BY register_date, index_name;