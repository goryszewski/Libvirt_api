# from pymongo import MongoClient
from mongoengine import connect


def init_mongo(config):
    required_keys = ["db", "host", "login", "password"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    connect(
        db=config["db"],
        host=config["host"],
        port=27017,
        username=config["login"],
        password=config["password"],
    )
