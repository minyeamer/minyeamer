-- ## 이차원 테이블에 대해 제곱 평균 제곱근(유클리드 거리)을 구하는 쿼리 ##
SELECT SQRT(POWER(x1 - x2, 2) + POWER(y1 - y2, 2)) AS dist
FROM location_2d;