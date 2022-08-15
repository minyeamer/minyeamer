-- ## 날짜별 매출과 평균 구매액을 집계하는 쿼리 ##
SELECT dt
	 , COUNT(*) AS purchase_count
	 , SUM(purchase_amount) AS total_amount
	 , AVG(purchase_amount * 1.0) AS avg_amount
FROM purchase_log
GROUP BY dt
ORDER BY dt;