from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager


class UserManager:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def login(self, email: str, password: str) -> tuple:
        with MySQLCursorContextManager(self.mysql) as cursor:
            select_query = "SELECT email, password FROM users WHERE email = %s AND password = %s"
            cursor.execute(select_query, (email, password))
            result = cursor.fetchone()
            yield result

    def register_user(self, email: str, password: str, phone_number: str) -> None:
        with MySQLCursorContextManager(self.mysql) as cursor:
            register_user_query = "INSERT INTO users (email, password, phone_number) VALUES (%s, %s, %s)"
            cursor.execute(register_user_query, (email, password, phone_number))

