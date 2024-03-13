from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager
from datetime import date, datetime


def add_expense(user_id: int, amount: int, paid_date: date, paid_to: str, remark: str,
                mysql: MySQL) -> bool:
    """insert the expense data """
    entry_date = date.today()
    with MySQLCursorContextManager(mysql) as cursor:
        insert_expense_query = "INSERT INTO expense (entry_date, paid_date, amount, userID, remark, paid_to) values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_expense_query, (entry_date, paid_date, amount, user_id, remark, paid_to))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def delete_expense(userID: int, expenseID: int, mysql: MySQL) -> None:
    """delete the expense id from the table by userID and expenseID"""
    with MySQLCursorContextManager(mysql) as cursor:
        delete_expense_query = "DELETE FROM expense WHERE userID=%s and expenseID=%s"
        cursor.execute(delete_expense_query, (userID, expenseID))


def get_all_expenses(user_id: int, mysql: MySQL) -> list[dict]:
    """returns the list of expenses related to the user id"""
    with MySQLCursorContextManager(mysql) as cursor:
        get_all_query = "SELECT * FROM expense where userID=%s ORDER BY expenseID desc"
        cursor.execute(get_all_query, (user_id,))
        results = cursor.fetchall()
        data: list[dict] = []
        for result in results:
            datum: dict = {
                "expense_id": result[0],
                "entry_date": result[1],
                "paid_date": result[2],
                "amount": result[3],
                "user_id": result[4],
                "remark": result[5],
                "paid_to": result[6]
            }
            data.append(datum)
        return data


def get_total_expense(user_id: int, mysql: MySQL) -> str:
    """returns the total amount of expenses of the user"""
    with MySQLCursorContextManager(mysql) as cursor:
        total_expense_query = 'SELECT sum(amount) FROM expense WHERE userID=%s'
        cursor.execute(total_expense_query, (user_id,))
        result = cursor.fetchone()
        if result[0] is not None and result:
            return format(result[0], ',')
        else:
            return '0'
