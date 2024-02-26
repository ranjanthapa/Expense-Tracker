from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager


def add_category(category_type: str, userID: int, mysql: MySQL) -> None:
    """insert the expense category or type"""
    with MySQLCursorContextManager(mysql) as cursor:
        select_category_query = "SELECT category_name from category where category_name=%s AND userID=%s"
        cursor.execute(select_category_query, category_type)
        category_exists = cursor.fetchone()
        if not category_exists:
            insert_category_query = "INSERT INTO category (category_name, userID) values(%s, %s)"
            cursor.execute(insert_category_query, (category_type, userID))


def add_expense(amount: int, categoryID: int, userID: int, remark: str, mysql: MySQL) -> None:
    """insert the expense data """
    with MySQLCursorContextManager(mysql) as cursor:
        insert_expense_query = "INSERT INTO expense (userID, amount, categoryID, remark) values(%s, %s, %s, %s)"
        cursor.execute(insert_expense_query, (userID, amount, categoryID, remark))


def delete_expense(userID: int, expenseID: int, mysql: MySQL) -> None:
    """delete the expense id from the table by userID and expenseID"""
    with MySQLCursorContextManager(mysql) as cursor:
        delete_expense_query = "DELETE FROM expense WHERE userID=%s and expenseID=%s"
        cursor.execute(delete_expense_query, (userID, expenseID))

