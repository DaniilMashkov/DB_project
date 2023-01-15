-- Выбрать все заказы, отсортировать по required_date и дате отгрузки
SELECT order_id, required_date, shipped_date, freight, ship_country FROM orders
ORDER BY required_date DESC, shipped_date;

-- Найти среднее значение дней уходящих на доставку с даты формирования заказа в USA
SELECT ROUND(AVG(shipped_date - order_date))
FROM orders
WHERE ship_country = 'USA';

-- Найти (количество * цену) товаров, которые не сняты с продажи
SELECT SUM(units_in_stock * unit_price) as total_product_sum
FROM products
WHERE DISCONTINUED = 0;