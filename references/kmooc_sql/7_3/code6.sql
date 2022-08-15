-- ## 정착률 지표를 관리하는 마스터 테이블을 작성하는 쿼리 ##
WITH
	repeat_interval AS (	SELECT '07 day retention' AS index_name,  1 AS interval_begin_date,  7 AS interval_end_date UNION ALL
							SELECT '14 day retention' AS index_name,  8 AS interval_begin_date, 14 AS interval_end_date UNION ALL
							SELECT '21 day retention' AS index_name, 15 AS interval_begin_date, 21 AS interval_end_date UNION ALL
							SELECT '28 day retention' AS index_name, 22 AS interval_begin_date, 28 AS interval_end_date	)
SELECT *
FROM repeat_interval
ORDER BY index_name;