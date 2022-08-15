-- ## 마스터 테이블의 행 수를 변경하지 않고 여러 개의 테이블을 가로로 정렬하는 쿼리 ##
SELECT m.category_id
	 , m.name
	 , s.sales
	 , r.product_id AS sale_product
FROM mst_categories AS m
LEFT OUTER JOIN category_sales AS s
	ON m.category_id = s.category_id
LEFT OUTER JOIN product_sale_ranking AS r
	ON m.category_id = r.category_id AND r.rank = 1;