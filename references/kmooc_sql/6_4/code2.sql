-- ## ROLLUP을 사용해서 카테고리별 매출과 소계를 동시에 구하는 쿼리 ##
SELECT COALESCE(category, 'all') AS category
	 , COALESCE(sub_category, 'all') AS sub_category
	 , SUM(price) AS amount
FROM purchase_detail_log
GROUP BY ROLLUP(category, sub_category);
-- < Hive >
-- GROUP BY category, sub_category WITH ROLLUP