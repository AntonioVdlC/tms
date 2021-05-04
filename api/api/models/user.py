from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.write_concern import WriteConcern

from datetime import datetime
import json

from api.utils.db import get_db


class User(object):
    def __init__(self, email: str, first_name: str, last_name: str, created_at: datetime, updated_at: datetime,
                 object_id: ObjectId = None, organisations: list = [], is_deleted: bool = False):
        self.object_id = object_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.organisations = organisations
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted

    def as_dict(self, to_cache=False):
        user_dict = {"email": self.email, "first_name": self.first_name, "last_name": self.last_name,
                     "organisations": self.organisations, "is_deleted": self.is_deleted}
        if to_cache:
            user_dict['_id'] = str(self.object_id)
            user_dict['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            user_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            user_dict['_id'] = self.object_id
            user_dict['created_at'] = self.created_at
            user_dict['updated_at'] = self.updated_at
        return user_dict

    @staticmethod
    def from_dict(user_dict, from_cache=False):
        if from_cache:
            object_id = ObjectId(user_dict['_id'])
            created_at = datetime.strptime(user_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            updated_at = datetime.strptime(user_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
            return User(object_id=object_id, email=user_dict['email'], first_name=user_dict['first_name'],
                        last_name=user_dict['last_name'], organisations=user_dict['organisations'],
                        is_deleted=user_dict['is_deleted'], created_at=created_at, updated_at=updated_at)
        else:
            return User(object_id=user_dict['_id'], email=user_dict['email'], first_name=user_dict['first_name'],
                        last_name=user_dict['last_name'], organisations=user_dict['organisations'],
                        is_deleted=user_dict['is_deleted'], created_at=user_dict['created_at'],
                        updated_at=user_dict['updated_at'])


def get_user_by_email(email: str) -> User:
    user_dict = get_db().users.find_one({"email": email, "is_deleted": False})
    if user_dict is None:
        return None
    else:
        return User.from_dict(user_dict)


def get_user_by_id(object_id: str) -> User:
    user_dict = get_db().users.find_one({"_id": ObjectId(object_id), "is_deleted": False})
    if user_dict is None:
        return None
    else:
        return User.from_dict(user_dict)


def insert_user(email: str, first_name: str, last_name: str) -> User:
    created_at = updated_at = datetime.utcnow()
    user = User(object_id=ObjectId(), email=email, first_name=first_name,
                last_name=last_name, created_at=created_at, updated_at=updated_at)
    get_db().users.with_options(write_concern=WriteConcern(w="majority")).insert_one(user.as_dict())
    return user


def add_organisation_to_user(user_id: str, org_id: str, session):
    get_db().users.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(user_id)}, {'$push': {'organisations': org_id}}, session=session)


def update_user_details(user_id: str, first_name: str, last_name: str) -> UpdateResult:
    result: UpdateResult = get_db().users.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(user_id)},
                    {'$set': {'first_name': first_name,
                              'last_name': last_name,
                              'updated_at': datetime.utcnow()}},
                    upsert=False)
    return result


def update_user_email(user_id: str, email: str) -> UpdateResult:
    result: UpdateResult = get_db().users.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(user_id)},
                    {'$set': {'email': email,
                              'updated_at': datetime.utcnow()}},
                    upsert=False)
    return result


def soft_delete_user(user_id: str, hashed_email: str, hashed_last_name: str) -> UpdateResult:
    result: UpdateResult = get_db().users.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(user_id)},
                    {'$set': {'email': hashed_email,
                              'last_name': hashed_last_name,
                              'is_deleted': True,
                              'updated_at': datetime.utcnow()}},
                    upsert=False)
    return result
