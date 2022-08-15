-- ## 행으로 저장된 지표 값을 열로 변환하는 쿼리 ##
SELECT dt
	 , MAX(CASE WHEN indicator = 'impressions'	THEN val END) AS impressions
	 , MAX(CASE WHEN indicator = 'sessions'		THEN val END) AS [sessions]
	 , MAX(CASE WHEN indicator = 'users'		THEN val END) AS users
FROM daily_kpi
GROUP BY dt
ORDER BY dt;