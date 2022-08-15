-- ## 각 단계에서의 리드 타임과 토탈 리드 타임을 계산하는 쿼리 ##
WITH
	requests AS (	SELECT 'U001' AS user_id, '1' AS product_id, '2016-09-01' AS request_date UNION ALL
					SELECT 'U001' AS user_id, '2' AS product_id, '2016-09-20' AS request_date UNION ALL
					SELECT 'U002' AS user_id, '3' AS product_id, '2016-09-30' AS request_date UNION ALL
					SELECT 'U003' AS user_id, '4' AS product_id, '2016-10-01' AS request_date UNION ALL
					SELECT 'U004' AS user_id, '5' AS product_id, '2016-11-01' AS request_date	),
	estimates AS (	SELECT 'U001' AS user_id, '2' AS product_id, '2016-09-21' AS estimate_date UNION ALL
					SELECT 'U002' AS user_id, '3' AS product_id, '2016-10-15' AS estimate_date UNION ALL
					SELECT 'U003' AS user_id, '4' AS product_id, '2016-10-15' AS estimate_date UNION ALL
					SELECT 'U004' AS user_id, '5' AS product_id, '2016-12-01' AS estimate_date	),
	orders AS (	SELECT 'U001' AS user_id, '2' AS product_id, '2016-10-01' AS order_date UNION ALL
				SELECT 'U004' AS user_id, '5' AS product_id, '2016-12-05' AS order_date	)
SELECT r.user_id
	 , r.product_id
	-- < SQLServer >
	 , DATEDIFF(DD, CAST(r.request_date AS DATE), CAST(e.estimate_date AS DATE)) AS estimate_lead_time
	 , DATEDIFF(DD, CAST(e.estimate_date AS DATE), CAST(o.order_date AS DATE)) AS order_lead_time
	 , DATEDIFF(DD, CAST(r.request_date AS DATE), CAST(o.order_date AS DATE)) AS total_lead_time
	-- < PostgreSQL, Redshift >
	-- e.estimate_date::date - r.request_date::date AS estimate_lead_time
	-- o.order_date::date - e.estimate_date::date AS order_lead_time
	-- o.order_date::date - r.request_date::date AS total_lead_time
	-- < BigQuery >
	-- date_diff(date(timestamp(e.estimate_date)), date(timestamp(r.request_date)), day) AS estimate_lead_time
	-- date_diff(date(timestamp(o.order_date)), date(timestamp(e.estimate_date)), day) AS order_lead_time
	-- date_diff(date(timestamp(o.order_date)), date(timestamp(r.request_date)), day) AS total_lead_time
	-- < Hive, SparkSQL >
	-- datediff(to_date(e.estimate_date), to_date(r.request_date)) AS estimate_lead_time
	-- datediff(to_date(o.order_date), to_date(e.estimate_date)) AS order_lead_time
	-- datediff(to_date(o.order_date), to_date(r.request_date)) AS total_lead_time
FROM requests AS r
LEFT OUTER JOIN estimates AS e
	ON r.user_id = e.user_id AND r.product_id = e.product_id
LEFT OUTER JOIN orders AS o
	ON r.user_id = o.user_id AND r.product_id = o.product_id;