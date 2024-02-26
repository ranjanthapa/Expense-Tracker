from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager


def income(userID: int, amount: int, source: str, remark: str, mysql: MySQL) -> None:
    with MySQLCursorContextManager(mysql) as cursor:
        insert_income: str = "INSERT INTO income (userID, amount, source, remark) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_income, (userID, amount, source, remark))


def get_total_income(userID: int, mysql: MySQL) -> tuple:
    with MySQLCursorContextManager(mysql) as cursor:
        total_income_query = "SELECT sum(amount) from income WHERE userID=%s"
        cursor.execute(total_income_query, (userID,))
        result = cursor.fetchone()
        return result
