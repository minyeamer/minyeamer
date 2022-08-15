-- ## 지속률 지표를 관리하는 마스터 테이블을 정착률 형식으로 수정한 쿼리 ##
WITH
	repeat_interval AS (	SELECT '01 day repeat' AS index_name, 1 AS interval_begin_date, 1 AS interval_end_date UNION ALL
							SELECT '02 day repeat' AS index_name, 2 AS interval_begin_date, 2 AS interval_end_date UNION ALL
							SELECT '03 day repeat' AS index_name, 3 AS interval_begin_date, 3 AS interval_end_date UNION ALL
							SELECT '04 day repeat' AS index_name, 4 AS interval_begin_date, 4 AS interval_end_date UNION ALL
							SELECT '05 day repeat' AS index_name, 5 AS interval_begin_date, 5 AS interval_end_date UNION ALL
							SELECT '06 day repeat' AS index_name, 6 AS interval_begin_date, 6 AS interval_end_date UNION ALL
							SELECT '07 day repeat' AS index_name, 7 AS interval_begin_date, 7 AS interval_end_date UNION ALL
							SELECT '07 day retention' AS index_name,  1 AS interval_begin_date,  7 AS interval_end_date UNION ALL
							SELECT '14 day retention' AS index_name,  8 AS interval_begin_date, 14 AS interval_end_date UNION ALL
							SELECT '21 day retention' AS index_name, 15 AS interval_begin_date, 21 AS interval_end_date UNION ALL
							SELECT '28 day retention' AS index_name, 22 AS interval_begin_date, 28 AS interval_end_date	)
SELECT *
FROM repeat_interval
ORDER BY index_name;