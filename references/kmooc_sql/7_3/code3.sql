-- ## 다음날 지속률을 계산하는 쿼리 ##
WITH
	action_log_with_mst_users AS (	SELECT u.user_id
										 , u.register_date
										 , CAST(a.stamp AS DATE) AS action_date
										 , MAX(CAST(a.stamp AS DATE)) OVER() AS latest_date
										-- < BigQuery >
										-- date(timestamp(a.stamp)) AS action_date
										-- MAX(date(timestamp(a.stamp))) OVER() AS latest_date
										-- < SQLServer > 
										 , CAST(DATEADD(DD, 1, u.register_date) AS DATE) AS next_day_1
										-- < PostgreSQL >
										-- CAST(u.register_date::date + '1 day'::interval AS date) AS next_day_1
										-- < Redshift >
										-- dateadd(day, 1, u.register_date::date) AS next_day_1
										-- < BigQuery >
										-- date_add(CAST(u.register_date AS date), interval 1 day) AS next_day_1
										-- < Hive, SparkSQL >
										-- date_add(CAST(u.register_date AS date), 1) AS next_day_1
									FROM mst_users AS u
									LEFT OUTER JOIN action_log AS a
										ON u.user_id = a.user_id	),
	user_action_flag AS (	SELECT user_id
								 , register_date
								 , SIGN(SUM(CASE WHEN next_day_1 <= latest_date THEN
												CASE WHEN next_day_1 = action_date THEN 1 ELSE 0 END
											END)) AS next_1_day_action
							FROM action_log_with_mst_users
							GROUP BY user_id, register_date	)
SELECT register_date
	 , AVG(100.0 * next_1_day_action) AS repeat_rate_1_day
FROM user_action_flag
GROUP BY register_date
ORDER BY register_date;