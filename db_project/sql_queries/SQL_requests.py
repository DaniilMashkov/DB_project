class SQLRequests:

    create_products_table = '''
        CREATE TABLE products(
        product_id smallserial PRIMARY KEY ,
        product_name VARCHAR(50),
        supplier_id int2 REFERENCES suppliers(supplier_id),
        category_id int2 REFERENCES categories(category_id),
        quantity_per_unit VARCHAR(50),
        unit_price DOUBLE PRECISION,
        units_in_stock int4,
        units_in_order int4,
        reorder_level int4,
        discontinued int2);'''

    create_suppliers_table ='''
        CREATE TABLE suppliers(
        supplier_id smallserial PRIMARY KEY,
        company_name VARCHAR(50),
        contact_name VARCHAR(50),
        contact_title VARCHAR(50),
        address VARCHAR(50),
        city VARCHAR(50),
        region VARCHAR(50),
        postal_code VARCHAR(15),
        country VARCHAR(50),
        phone VARCHAR(15),
        fax VARCHAR(15),
        homepage VARCHAR(150)
        )'''

    fill_suppliers = f"INSERT INTO suppliers VALUES({('%s, ' * 12).rstrip(', ')})"

    get_products = f"SELECT * FROM products"

    fill_products = f"INSERT INTO products VALUES ({('%s, ' * 10).rstrip(', ')})"

    drop_old_products = f"DROP TABLE products CASCADE"

    restore_reference_in_order_details = '''ALTER TABLE order_details ADD CONSTRAINT fk_order_details_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)'''

    drop_schema = "DROP SCHEMA public CASCADE"

    create_schema = "CREATE SCHEMA public"

    @staticmethod
    def get_by_product_id(key):
        return f'''SELECT product_id, product_name, categories.category_name, unit_price 
                FROM products INNER JOIN categories USING(category_id) WHERE product_id = {key}'''

    @staticmethod
    def get_by_category_id(key):
        return f'''select category_id, category_name, description, product_name from categories "
                        f"inner join products using(category_id) where category_id = {key}'''