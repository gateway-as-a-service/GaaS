import datetime

from pymongo import MongoClient

from receivers.config import MONGO_DB_PORT, MONGO_DB_HOSTNAME


class MongoUtils(object):
    client = MongoClient(MONGO_DB_HOSTNAME, MONGO_DB_PORT)
    gass_database = client["gass"]
    devices = gass_database["devices"]
    rules = gass_database["rules"]


def get_utc_timestamp():
    return datetime.datetime.utcnow().timestamp()