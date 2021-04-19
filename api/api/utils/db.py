from pymongo import MongoClient
from flask import current_app

_db: MongoClient = None


def init_db():
    global _db
    if _db is None:
        current_app.logger.info("Setting up db..")
        _db = MongoClient(current_app.config['MONGO_HOST'])


def get_db() -> MongoClient:
    global _db
    return _db.tms

