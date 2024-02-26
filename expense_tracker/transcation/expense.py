from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager


def insert_category(category_type: str, mysql: MySQL) -> None:
    with MySQLCursorContextManager(mysql) as cursor:
        select_category_query = "SELECT category_name from category where category_name=%s"
        cursor.execute(select_category_query, category_type)
        category_exists = cursor.fetchone()
        if not category_exists:
            insert_category_query = "INSERT INTO category (category_name) values(%s)"
            cursor.execute(insert_category_query, category_type)


def insert_expense(amount: int, categoryID: int, userID: int, remark: str, mysql: MySQL) -> None:
    with MySQLCursorContextManager(mysql) as cursor:
        insert_expense_query = "INSERT INTO expense (userID, amount, categoryID, remark) values(%s, %s, %s, %s)"
        cursor.execute(insert_expense_query, (userID, amount, categoryID, remark))
