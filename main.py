from db_project.utils import *
from psycopg2 import connect
from config import config


def main():
    conn = connect(config)

    opt, index = pick(title='Выберете действие: ',
                      options=(' Заполнить таблицу suppliers', ' SQL Запросы',
                               ' Запрос по product_id', ' Запрос по category_id',
                               ' Восстановить исходное состояние БД', ' #Выход'))
    match index:
        case 0:
            try:
                fill_tables(conn)
                print('Done')
            except Exception as ex:
                print(ex)
        case 1:
            get_from_db(conn, main)
        case 2:
            get_by_id(conn, 'product_id')
        case 3:
            get_by_id(conn, 'category_id')
        case 4:
            restore_db(conn)
            print('Done')
        case 5:
            exit()
    if not input('\nEnter продолжить | Любой символ для выхода\n'):
        main()

    conn.close()


if __name__ == '__main__':
    main()
