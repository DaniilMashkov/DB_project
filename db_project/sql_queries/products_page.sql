-- Активные продукты из категории Beverages и Seafood, наличие менее 20 единиц.
SELECT product_name, units_in_stock, suppliers.contact_name, suppliers.phone
FROM products
JOIN categories ON categories.category_id = products.category_id
JOIN suppliers ON suppliers.supplier_id = products.supplier_id
WHERE categories.category_name in ('Beverages', 'Seafood')
AND products.discontinued = 0 AND products.units_in_stock < 20;