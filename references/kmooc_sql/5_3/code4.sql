-- ## 0으로 나누는 것을 피해 CTR을 계산하는 쿼리 ##
SELECT dt
	 , ad_id
	-- 0으로 나누기 오류 발생
	-- 100.0 * clicks / impressions AS ctr_as_percent
	 , CASE WHEN impressions > 0 THEN 100.0 * clicks / impressions END AS ctr_as_percent_by_case
FROM advertising_stats
ORDER BY dt, ad_id;