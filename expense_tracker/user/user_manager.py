import MySQLdb
from flask_mysqldb import MySQL
from expense_tracker.mysql_context import MySQLCursorContextManager
from flask import request
from expense_tracker.utils import is_allowed_file, get_media_folder_path, get_hash_password
from .exception import UserExists
from werkzeug.utils import secure_filename
import os
from flask_login import UserMixin, login_user


class User(UserMixin):
    def __init__(self, user_data: dict):
        self.user_data = user_data

    def get_id(self):
        return self.user_data.get('user_id')

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


class UserManager:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def login(self, email: str, password: str) -> bool:
        hash_password = get_hash_password(password)
        with MySQLCursorContextManager(self.mysql) as cursor:
            select_query = "SELECT userID FROM users WHERE email = %s AND password = %s"
            cursor.execute(select_query, (email, hash_password))
            result = cursor.fetchone()
            if result:
                user = User({
                    "user_id": result[0]
                })
                login_user(user)
                return True

            else:
                return False

    def register_user(self, email: str, password: str, phone_number: str, full_name: str) -> None:
        image_file = request.files['profile_picture']
        image_save_path = self.handle_upload_file(image_file)
        hash_password = get_hash_password(password)
        with MySQLCursorContextManager(self.mysql) as cursor:
            register_user_query = "INSERT INTO users (email, password, phone_number, full_name, profile_picture) VALUES (%s, %s, %s, %s, %s)"
            try:
                cursor.execute(register_user_query, (email, hash_password, phone_number, full_name, image_save_path))
            except MySQLdb.IntegrityError:
                raise UserExists("User with the same email exists")

    @staticmethod
    def handle_upload_file(image_file):
        """handles the upload file e.g. images for storing and return the path of storage
            :param image_file: the image file that is to be store
            :type image_file: werkzeug.datastructures.file_storage.FileStorage
        """

        if image_file and is_allowed_file(image_file.filename):
            file_name = secure_filename(image_file.filename)
            media_path = get_media_folder_path()
            os.makedirs(media_path, exist_ok=True)
            print(media_path)
            image_save_path = os.path.join(media_path, file_name)
            image_file.save(image_save_path)
        else:
            image_save_path = None
        return image_save_path

    def get_user_info(self, user_id: int) -> dict:
        with MySQLCursorContextManager(self.mysql) as cursor:
            get_user_query = "SELECT * FROM users WHERE userID=%s"
            cursor.execute(get_user_query, (user_id,))
            result = cursor.fetchone()
            if result:
                data = {
                    "user_id": result[0],
                    "email": result[1],
                    "phone_number": result[3],
                    "full_name": result[4],
                    "profile_pic": result[5].replace('\\', '/')
                }
                return data

    def update_profile(self, user_id, data: dict):
        with MySQLCursorContextManager(self.mysql) as cursor:
            update_profile_query = "UPDATE users SET "
            values: list = []
            for key, value in data.items():
                if value:
                    update_profile_query += f"{key}=%s,"
                    if key == "password":
                        value = get_hash_password(value)
                    values.append(value)
            image_file = request.files['profile_picture']
            if image_file:
                profile_path = self.handle_upload_file(image_file)
                update_profile_query += "profile_picture=%s,"
                values.append(profile_path)

            print(update_profile_query)
            update_profile_query = update_profile_query.rstrip(',')
            print(update_profile_query)
            update_profile_query += " WHERE userID = %s"
            values.append(user_id)
            cursor.execute(update_profile_query, tuple(values))
            if cursor.rowcount > 0:
                return True
            else:
                return False
