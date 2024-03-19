# from pymongo import MongoClient
from mongoengine import connect


def init_mongo(config):
    connect(db=config['db'],host=config['host'],port=27017,username=config['login'],password=config['password'])
