import hashlib
import os

__ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}


def get_hash_password(password: str) -> str:
    """hashing the password"""
    hash_psw = hashlib.sha256(password.encode()).hexdigest()
    return hash_psw


def get_media_folder_path() -> str:
    """gives the media folder path to store the user's file i.e. image and other"""
    current_dir = os.getcwd()
    media_folder = os.path.abspath(os.path.join(current_dir, 'media', 'profile_pictures'))
    return media_folder


def get_allowed_extension() -> set:
    """gives the set of allowed extension for the file """
    return __ALLOWED_EXTENSIONS


def is_allowed_file(filename: str) -> bool:
    """checks the filename is included in allowed extension or not"""
    allowed_extensions = get_allowed_extension()
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions
