from flask_mysqldb import MySQL


class DatabaseConfig:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '@dmin123'
    MYSQL_DB = 'expense_tracker'


def initialize_sql(app):
    mysql = MySQL(app)
    return mysql
