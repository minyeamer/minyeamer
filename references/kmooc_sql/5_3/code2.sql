-- ## 평균 4분기 매출을 구하는 쿼리 ##
SELECT year
	 , (q1 + q2 + q3 + q4) / 4 AS average1
	 , (COALESCE(q1, 0) + COALESCE(q2, 0) + COALESCE(q3, 0) + COALESCE(q4, 0)) / 4 AS average2
	 , (COALESCE(q1, 0) + COALESCE(q2, 0) + COALESCE(q3, 0) + COALESCE(q4, 0)) /
	   (SIGN(COALESCE(q1, 0)) + SIGN(COALESCE(q2, 0)) + SIGN(COALESCE(q3, 0)) + SIGN(COALESCE(q4, 0))) AS average3
FROM quarterly_sales
ORDER BY year;