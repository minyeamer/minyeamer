-- ## q1, q2 컬럼을 비교하는 쿼리 ##
SELECT year
	 , q1
	 , q2
	 , CASE WHEN q1 < q2 THEN '+'
			WHEN q1 = q2 THEN ' '
			ELSE '-' END AS judge_q1_q2
	 , q2 - q1 AS diff_q2_q1
	 , SIGN(q2 - q1) AS sign_q2_q1
FROM quarterly_sales
ORDER BY year;