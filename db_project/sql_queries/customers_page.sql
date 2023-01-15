-- Посчитать количество заказчиков
SELECT COUNT(customer_id)
FROM customers;

-- Выбрать все города и страны, в которых "зарегестрированы" заказчики
SELECT country, city
FROM customers
GROUP BY country, city;

-- Найти заказчиков и сотрудников из London, доставка Speedy Express
SELECT customers.company_name as company, employees.first_name as name, employees.last_name as surname
FROM orders
JOIN customers ON customers.customer_id = orders.customer_id
JOIN employees ON employees.employee_id = orders.employee_id
JOIN shippers ON shippers.shipper_id = orders.ship_via
WHERE customers.city = 'London' AND employees.city = 'London' AND shippers.company_name = 'Speedy Express';

-- Найти заказчиков, не сделавших ни одного заказа
SELECT company_name, orders.order_id
FROM customers
LEFT JOIN orders ON orders.customer_id = customers.customer_id
WHERE orders.order_id IS NULL;