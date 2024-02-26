from flask_mysqldb import MySQL


class MySQLCursorContextManager:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def __enter__(self):
        self.cursor = self.mysql.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.connection.commit()
        self.cursor.close()
