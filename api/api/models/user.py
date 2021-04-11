from bson.objectid import ObjectId
from pymongo.results import InsertOneResult

from datetime import datetime
import json

from api.utils.db import get_db


class User(object):
    def __init__(self, object_id: ObjectId, email: str, first_name: str,
                 last_name: str, created_at: datetime, updated_at: datetime):
        self.object_id = object_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {"object_id": str(self.object_id), "email": self.email, "first_name": self.first_name,
                "last_name": self.last_name}


def get_user_by_email(email: str) -> User:
    user_dict = get_db().tms.users.find_one({"email": email})
    if user_dict is None:
        return None
    else:
        user = User(object_id=user_dict['_id'], email=user_dict['email'], first_name=user_dict['first_name'],
                    last_name=user_dict['last_name'], created_at=user_dict['created_at'],
                    updated_at=user_dict['updated_at'])
        return user


def insert_user(email: str, first_name: str, last_name: str) -> User:
    created_at = updated_at = datetime.utcnow()
    result: InsertOneResult = get_db().tms.users.insert_one({"email": email, "first_name": first_name,
                                                             "last_name": last_name, "created_at": created_at,
                                                             "updated_at": updated_at})
    return User(object_id=result.inserted_id, email=email, first_name=first_name,
                last_name=last_name, created_at=created_at, updated_at=updated_at)
