-- ## 여러 개의 테이블을 결합해서 가로로 정렬하는 쿼리 ##
SELECT m.category_id
	 , m.name
	 , s.sales
	 , r.product_id AS sale_product
FROM mst_categories AS m
INNER JOIN category_sales AS s
	ON m.category_id = s.category_id
INNER JOIN product_sale_ranking AS r
	ON m.category_id = r.category_id;