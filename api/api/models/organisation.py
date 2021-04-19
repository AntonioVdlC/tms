from bson.objectid import ObjectId
from pymongo.results import InsertOneResult

from datetime import datetime
from enum import Enum

from api.utils.db import get_db


class MemberType(str, Enum):
    admin = 'admin'
    developer = 'developer'
    translator = 'translator'


class Member(object):
    def __init__(self, user_id: str, member_type: MemberType, added_at: datetime):
        self.user_id = user_id
        self.member_type = member_type
        self.added_at = added_at

    def as_dict(self):
        return {"user_id": self.user_id, "member_type": self.member_type.value, "added_at": self.added_at}


class Organisation(object):
    def __init__(self, name: str, members: list, creator_id: str, created_at: datetime, updated_at: datetime,
                 is_deleted: bool, object_id: ObjectId = None):
        self.object_id = object_id
        self.name = name
        self.members = members
        self.creator_id = creator_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted

    def as_dict(self):
        members_list = list(map(lambda member: member.as_dict(), self.members))
        organisation_dict = {"name": self.name, "members": members_list,
                             "creator_id": self.creator_id, "created_at": self.created_at,
                             "updated_at": self.updated_at, "is_deleted": self.is_deleted}
        if self.object_id is not None:
            organisation_dict['object_id'] = str(self.object_id)
        return organisation_dict


def insert_organisation(name: str, creator_id: str):
    created_at = updated_at = added_at = datetime.utcnow()
    members = [Member(creator_id, MemberType.admin, added_at)]
    organisation = Organisation(name, members, creator_id, created_at, updated_at, False)
    result: InsertOneResult = get_db().organisations.insert_one(organisation.as_dict())
    organisation.object_id = result.inserted_id
    return organisation
