-- ## 날짜별 매출과 7일 이동평균을 집계하는 쿼리 ##
WITH
	purchase_by_day AS (	SELECT dt
								 , SUM(purchase_amount) AS amount
							FROM purchase_log
							GROUP BY dt	)
SELECT dt
	 , amount AS total_amount
	 , CASE WHEN 6 <= (SELECT DATEDIFF(DD, MIN(dt), MAX(dt)) FROM purchase_by_day AS s WHERE s.dt BETWEEN DATEADD(DD, -6, m.dt) AND m.dt)
			THEN (SELECT AVG(amount * 1.0) FROM purchase_by_day AS s WHERE s.dt BETWEEN DATEADD(DD, -6, m.dt) AND m.dt) END AS seven_day_avg
FROM purchase_by_day AS m
ORDER BY dt;