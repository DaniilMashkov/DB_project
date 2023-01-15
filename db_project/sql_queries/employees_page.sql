-- Выбрать записи работников в которых регион неизвестен
SELECT last_name, first_name, home_phone, region
FROM employees
WHERE region IS NULL;

-- Выбрать страны в которых "зарегистированы" заказчики и поставщики, но не работники
SELECT country FROM customers
INTERSECT
SELECT country FROM suppliers
EXCEPT
SELECT country FROM employees;