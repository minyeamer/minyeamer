-- ## 카테고리들의 순위에서 유니크한 순위 목록을 계산하는 쿼리 ##
WITH
	product_sale_ranking AS (	SELECT category_name
									 , product_id
									 , sales
									 , ROW_NUMBER() OVER(PARTITION BY category_name ORDER BY sales DESC) AS rank
								FROM product_sales	),
	mst_rank AS (	SELECT DISTINCT rank
					FROM product_sale_ranking	)
SELECT *
FROM mst_rank;