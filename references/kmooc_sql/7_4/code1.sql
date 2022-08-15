-- ## 신청일과 숙박일의 리드 타임을 계산하는 쿼리 ##
WITH
	reservations AS (	SELECT 1 AS reservation_id, '2016-09-01' AS register_date, '2016-10-01' AS visit_date, 3 AS [days]	UNION ALL
						SELECT 2 AS reservation_id, '2016-09-20' AS register_date, '2016-10-01' AS visit_date, 2 AS [days]	UNION ALL
						SELECT 3 AS reservation_id, '2016-09-30' AS register_date, '2016-11-20' AS visit_date, 2 AS [days]	UNION ALL
						SELECT 4 AS reservation_id, '2016-10-01' AS register_date, '2017-01-03' AS visit_date, 2 AS [days]	UNION ALL
						SELECT 5 AS reservation_id, '2016-11-01' AS register_date, '2016-12-28' AS visit_date, 3 AS [days]	)
SELECT reservation_id
	 , register_date
	 , visit_date
	-- < SQLServer >
	 , DATEDIFF(DD, CAST(register_date AS DATE), CAST(visit_date AS DATE)) AS lead_time
	-- < PostgreSQL, Redshift >
	-- visit_date::date - register_date::date AS lead_time
	-- < BigQuery >
	-- date_diff(date(timestamp(visit_date)), date(timestamp(register_date)), day) AS lead_time
	-- < Hive, SparkSQL >
	-- datediff(to_date(visit_date), to_date(register_date)) AS lead_time
FROM reservations;