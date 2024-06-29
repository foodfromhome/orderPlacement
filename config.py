import os
from pydantic import BaseConfig
from dotenv import load_dotenv

load_dotenv()


class GlobalConfig(BaseConfig):
    mongo_username = os.getenv("DB_USERNAME")
    mongo_password = os.getenv("DB_PASSWORD")
    mongo_host = os.getenv("DB_HOST")
    mongo_port = os.getenv("DB_PORT")
    mongo_db = os.getenv("DB_NAME")

    redis_host = os.getenv("REDIS_SERVER")
    redis_port = os.getenv("REDIS_PORT")


settings = GlobalConfig()
