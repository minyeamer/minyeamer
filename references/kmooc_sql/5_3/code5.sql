-- ## 일차원 데이터의 절댓값과 제곱 평균 제곱근을 계산하는 쿼리 ##
SELECT ABS(x1 - x2) AS [abs]
	 , SQRT(POWER(x1 - x2, 2)) AS rms
FROM location_1d;