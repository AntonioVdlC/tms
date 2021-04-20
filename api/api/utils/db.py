from pymongo import MongoClient
from pymongo.database import Database
from flask import current_app

_db: MongoClient = None


def init_db():
    global _db
    if _db is None:
        current_app.logger.info("Setting up db..")
        _db = MongoClient(current_app.config['MONGO_HOST'])


def get_db() -> Database:
    global _db
    return _db.tms


def get_client() -> MongoClient:
    global _db
    return _db

