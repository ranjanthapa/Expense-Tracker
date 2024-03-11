from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseConfig:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = 'expense_tracker'


def initialize_sql(app):
    mysql = MySQL(app)
    return mysql

