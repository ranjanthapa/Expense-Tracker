from flask_mysqldb import MySQL


def category(category_type: str, mysql: MySQL) -> None:
    cursor = mysql.connection.cursor()
    select_category_query = "SELECT category_name from category where category_name=%s"
    cursor.execute(select_category_query, category_type)
    category_exists = cursor.fetchone()
    if not category_exists:
        category_query = "INSERT INTO category (category_name) values(%s)"
        cursor.execute(category_query, category_type)
        cursor.connection.commit()
        cursor.close()
    else:
        cursor.close()


def expense(amount: int, categoryID: int, userID: int, remark: str, mysql: MySQL) -> None:
    cursor = mysql.connection.cursor()
    expense_query = "INSERT INTO expense (userID, amount, categoryID, remark) values(%s, %s, %s, %s)"
    cursor.execute(expense_query, (userID, amount, categoryID, remark))
    cursor.connection.commit()
    cursor.close()
