from db_project.GetSupplierInfo import GetSupplierInfo
from db_project.sql_queries.SQL_requests import SQLRequests
from psycopg2.extras import DictCursor
from tabulate import tabulate
from pick import pick
import pandas as pd
import re
import json


def fill_tables(conn) -> None:
    cur = conn.cursor()

    """ Создание и заполнение таблицы <suppliers>"""

    cur.execute(SQLRequests.create_suppliers_table)

    with open('data/suppliers.json', 'r') as file:
        for item in json.load(file):
            GetSupplierInfo.init(item)
            cur.execute(SQLRequests.fill_suppliers, GetSupplierInfo.to_tuple())

    """ Берёт значения из таблицы <products>, удаляет её и создаёт новую,
    добавив колонку product_id. Устанавливает все отношения, что были раньше."""

    cur.execute(SQLRequests.get_products)
    products = cur.fetchall()

    cur.execute(SQLRequests.drop_old_products)
    cur.execute(SQLRequests.create_products_table)

    for row in products:
        if row[1] in GetSupplierInfo.products_list.keys():
            updated = list(row)
            updated.insert(2, GetSupplierInfo.products_list.get(row[1]))
            cur.execute(SQLRequests.fill_products, tuple(updated))

    cur.execute(SQLRequests.restore_reference_in_order_details)

    conn.commit()
    cur.close()
    conn.close()


def get_from_db(conn, main):
    opt, index = pick(title='Выберете страницу', options=[
        ' «Заказчики» customers_page', ' «Заказы» orders_page',
        ' «Сотрудники» employees_page', ' «Товары» products_page', ' <- Назад'])

    match index:
        case 0:
            sql_parser(conn, 'db_project/sql_queries/customers_page.sql')
        case 1:
            sql_parser(conn, 'db_project/sql_queries/orders_page.sql')
        case 2:
            sql_parser(conn, 'db_project/sql_queries/employees_page.sql')
        case 3:
            sql_parser(conn, 'db_project/sql_queries/products_page.sql')
        case 4:
            main()


def sql_parser(conn, path: str):
    """ Парсинг sql файла:
        - Берёт комментарии из файла для вывода пользователю в меню
        - sql запрос передаёт в функцию 'return_sql_as_json' """

    cur = conn.cursor(cursor_factory=DictCursor)
    with open(path, 'r') as sql:
        raw = sql.read()
        comments = re.findall(r'--([\s\S]+?)\n|(--)', raw)
        comments = [x[0] for x in comments]
        parsed = re.sub(r'--([\s\S]+?)\n|(--)', '', raw)
        requests = re.split(r';\n', parsed)

        opt, index = pick(title='Выберете запрос', options=comments)
        cur.execute(requests[index])

        return_sql_as_json(cur)
        cur.close()


def get_by_id(conn, column_name: str):
    cur = conn.cursor(cursor_factory=DictCursor)
    case = input(f'\nВведите {column_name}:\n ')
    match column_name:
        case 'product_id':
            cur.execute(SQLRequests.get_by_product_id(case))
        case 'category_id':
            cur.execute(SQLRequests.get_by_category_id(case))

    return_sql_as_json(cur)
    cur.close()


def restore_db(conn):
    cur = conn.cursor()
    cur.execute(SQLRequests.drop_schema)
    cur.execute(SQLRequests.create_schema)
    with open('sql_queries/init_db.sql', 'r') as sql:
        raw = sql.read()
        parsed = re.sub(r'--([\s\S]+?)\n|(--)', '', raw)
        requests = re.split(r';\n', parsed)[:-1]
        for query in requests:
            cur.execute(query)
    conn.commit()
    cur.close()


def return_sql_as_json(cur):
    '''Принтит реультат и возвращает json строку'''

    response = [dict(x) for x in cur.fetchall()]
    df = pd.DataFrame.from_records(response)

    print(tabulate(df, headers='keys', tablefmt='github'))

    cur.close()
    return json.dumps(response, ensure_ascii=False, default=str)
