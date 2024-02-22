import unittest
from flask_mysqldb import MySQL


class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.mysql = MySQL

    def test_login(self):
        cursor = self.mysql.connection.cursor()
        email = "ranjanthapa123@gmail.com"
        password = '1234'
        select_query = "SELECT email, password FROM users WHERE email = %s AND password = %s"
        cursor.execute(select_query, (email, password))
        result = cursor.fetchone()
        cursor.close()
        assert self.assertIsNone(result)
        assert self.assertEqual(result[0], email)
        assert self.assertEqual(result[1], password)


if __name__ == '__main__':
    unittest.main()
