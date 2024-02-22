from flask_mysqldb import MySQL


def income(userID: int, amount: int, source: str, remark: str, mysql: MySQL):
    cursor = mysql.connection.cursor()
    income_query = "INSERT INTO income (userID, amount, source, remark) VALUES (%s, %s, %s, %s)"

    cursor.execute(income_query, (userID, amount, source, remark))
    cursor.connection.commit()
    cursor.close()


def get_total_income(userID: int, mysql: MySQL) -> tuple:
    cursor = mysql.connection.cursor()
    total_income_query = "SELECT sum(amount) from income WHERE userID=%s"
    cursor.execute(total_income_query, userID)
    result = cursor.fetchone()
    return result
