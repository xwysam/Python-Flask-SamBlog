#encoding: utf-8
import os

# dialect+driver://username:password@host:port/database

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'xwysam123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db1'


CACHE_TYPE =  'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = '6379'
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = ''


SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False


DEBUG = True

SECRET_KEY = os.urandom(24)
