-- ## 지속률 지표를 관리하는 마스터 테이블을 작성하는 쿼리 ##
WITH
	repeat_interval AS (	SELECT '01 day repeat' AS index_name, 1 AS interval_date UNION ALL
							SELECT '02 day repeat' AS index_name, 2 AS interval_date UNION ALL
							SELECT '03 day repeat' AS index_name, 3 AS interval_date UNION ALL
							SELECT '04 day repeat' AS index_name, 4 AS interval_date UNION ALL
							SELECT '05 day repeat' AS index_name, 5 AS interval_date UNION ALL
							SELECT '06 day repeat' AS index_name, 6 AS interval_date UNION ALL
							SELECT '07 day repeat' AS index_name, 7 AS interval_date )
SELECT *
FROM repeat_interval
ORDER BY index_name;