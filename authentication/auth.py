import os

import hashlib
import datetime
import psycopg2

from utils.constants import LOGIN_URL
from utils.common_class import APICaller
from utils.logger import get_console_logger

log = get_console_logger()


def generate_password() -> str:
    date_str = datetime.datetime.utcnow().strftime("%d%m%Y")
    base_string = date_str + os.environ.get("STORE_KEY")
    hashed = hashlib.sha256(base_string.encode("utf-8")).hexdigest().upper()
    password = hashed + os.environ.get("VENDOR_KEY")
    password = password.replace("&", "%26").replace("+", "%2B").replace("=", "%3D")

    return password


def retrieve_bearer_token() -> str:
    password = generate_password()

    api_caller = APICaller(
        url=f"{LOGIN_URL}/?username={os.environ.get('USERNAME')}&password={password}"
    )

    api_caller.post()

    token = api_caller.response.get("token")

    return token


def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
    )
    return conn
