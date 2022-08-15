-- ## 일련번호를 가진 피벗 테이블을 사용해 행으로 변환하는 쿼리 ##
SELECT q.[year]
	 , CASE WHEN p.idx = 1 THEN 'q1'
			WHEN p.idx = 2 THEN 'q2'
			WHEN p.idx = 3 THEN 'q3'
			WHEN p.idx = 4 THEN 'q4' END AS [quarter]
	 , CASE WHEN p.idx = 1 THEN q.q1
			WHEN p.idx = 2 THEN q.q2
			WHEN p.idx = 3 THEN q.q3
			WHEN p.idx = 4 THEN q.q4 END AS sales
FROM quarterly_sales AS q
CROSS JOIN (	SELECT 1 AS idx UNION ALL
				SELECT 2 AS idx UNION ALL
				SELECT 3 AS idx UNION ALL
				SELECT 4 AS idx	) AS p;