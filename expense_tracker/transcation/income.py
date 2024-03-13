from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager
from datetime import date


def add_income(user_id: int, amount: int, source: str, remark: str, mysql: MySQL,
               receive_date: date) -> bool:
    """insert the income"""
    entry_date = date.today()
    with MySQLCursorContextManager(mysql) as cursor:
        insert_income: str = "INSERT INTO income (userID, amount, source, remark, entry_date, receive_date) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_income, (user_id, amount, source, remark, entry_date, receive_date))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def get_total_income(user_id: int, mysql: MySQL) -> tuple:
    """returns the total income of userID"""
    with MySQLCursorContextManager(mysql) as cursor:
        total_income_query = "SELECT sum(amount) from income WHERE userID=%s"
        cursor.execute(total_income_query, (user_id,))
        result = cursor.fetchone()
        return result


def get_income_by_user_id(user_id: int, mysql: MySQL) -> list[dict]:
    """ returns the list of income related to the user id """
    with MySQLCursorContextManager(mysql) as cursor:
        get_income_query = "SELECT * FROM income WHERE userID=%s ORDER BY incomeID desc  "
        cursor.execute(get_income_query, (user_id,))
        results = cursor.fetchall()
        data: list[dict] = []
        for result in results:
            datum: dict = {
                'income_id': result[0],
                'user_id': result[1],
                'amount': result[2],
                'remark': result[3],
                'entry_date': result[4],
                'source': result[5],
                'receive_date': result[6]
            }
            data.append(datum)
        return data


def get_total_incomes(user_id: int, mysql: MySQL) -> str:
    """ returns the total amount of money receive """
    with MySQLCursorContextManager(mysql) as cursor:
        total_income_query = 'SELECT sum(amount) FROM income WHERE userID=%s'
        cursor.execute(total_income_query, (user_id,))
        result = cursor.fetchone()
        if result[0] is not None and result:
            return format(result[0], ',')

        else:
            return '0'
