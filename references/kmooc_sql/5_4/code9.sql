-- ## 카테고리별 순위를 추가한 테이블에 이름 붙이는 쿼리 ##
WITH
	product_sale_ranking AS (	SELECT category_name
									 , product_id
									 , sales
									 , ROW_NUMBER() OVER(PARTITION BY category_name ORDER BY sales DESC) AS rank
								FROM product_sales	)
SELECT *
FROM product_sale_ranking;