from flask_mysqldb import MySQL


class UserManager:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def login(self, email: str, password: str) -> tuple:
        cursor = self.mysql.connection.cursor()
        select_query = "SELECT email, password FROM users WHERE email = %s AND password = %s"
        cursor.execute(select_query, (email, password))
        result = cursor.fetchone()
        cursor.close()
        return result

    def register_user(self, email: str, password: str, phone_number: str) -> None:
        cursor = self.mysql.connection.cursor()
        insert_query = "INSERT INTO users (email, password, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (email, password, phone_number))
        self.mysql.connection.commit()
        cursor.close()
