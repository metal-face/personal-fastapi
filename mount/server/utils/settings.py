import os

from dotenv import load_dotenv

load_dotenv()

APP_COMPONENT = os.environ["APP_COMPONENT"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])
APP_ENV = os.environ["APP_ENV"]

DB_DRIVER = os.environ["DB_DRIVER"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_NAME = os.environ["DB_NAME"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_DB = int(os.environ["REDIS_DB"])

RECAPTCHA_SECRET_KEY = os.environ["RECAPTCHA_SECRET_KEY"]
RECAPTCHA_SITE_KEY = os.environ["RECAPTCHA_SITE_KEY"]
