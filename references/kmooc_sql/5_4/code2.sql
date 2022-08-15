-- ## 구매액에서 할인 쿠폰 값을 제외한 매출 금액을 구하는 쿼리 ##
SELECT purchase_id
	 , amount
	 , coupon
	 , amount - coupon AS discount_amount1
	 , amount - COALESCE(coupon, 0) AS discount_amount2
FROM purchase_log_with_coupon;