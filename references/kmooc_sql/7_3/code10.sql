-- ## 12개월 후까지의 월을 도출하기 위한 보조 테이블을 만드는 쿼리 ##
WITH
	mst_intervals AS (	SELECT  1 AS interval_month UNION ALL
						SELECT  2 AS interval_month UNION ALL
						SELECT  3 AS interval_month UNION ALL
						SELECT  4 AS interval_month UNION ALL
						SELECT  5 AS interval_month UNION ALL
						SELECT  6 AS interval_month UNION ALL
						SELECT  7 AS interval_month UNION ALL
						SELECT  8 AS interval_month UNION ALL
						SELECT  9 AS interval_month UNION ALL
						SELECT 10 AS interval_month UNION ALL
						SELECT 11 AS interval_month UNION ALL
						SELECT 12 AS interval_month	)
SELECT *
FROM mst_intervals;