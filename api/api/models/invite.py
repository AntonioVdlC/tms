from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.write_concern import WriteConcern

from datetime import datetime

from api.utils.db import get_db
from api.models.organisation import MemberType
from api.utils.app_wrapper import get_logger


class Invite(object):
    def __init__(self, email: str, member_type: MemberType, org_id: str, created_at: datetime, updated_at: datetime,
                 is_deleted: bool = False, object_id: ObjectId = None):
        self.object_id = object_id
        self.email = email
        self.member_type = member_type
        self.org_id = org_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted

    def as_dict(self, to_cache=False):
        invite_dict = {"email": self.email, "member_type": self.member_type.value, "org_id": self.org_id,
                       "is_deleted": self.is_deleted}
        if to_cache:
            invite_dict['_id'] = str(self.object_id)
            invite_dict['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            invite_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            invite_dict['_id'] = self.object_id
            invite_dict['created_at'] = self.created_at
            invite_dict['updated_at'] = self.updated_at
        return invite_dict

    @staticmethod
    def from_dict(invite_dict, from_cache=False):
        if from_cache:
            object_id = ObjectId(invite_dict['_id'])
            created_at = datetime.strptime(invite_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            updated_at = datetime.strptime(invite_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
            return Invite(object_id=object_id, email=invite_dict['email'],
                          member_type=MemberType[invite_dict['member_type']], org_id=invite_dict['org_id'],
                          created_at=created_at, updated_at=updated_at, is_deleted=invite_dict['is_deleted'])
        else:
            return Invite(object_id=invite_dict['_id'], email=invite_dict['email'],
                          member_type=MemberType[invite_dict['member_type']], org_id=invite_dict['org_id'],
                          created_at=invite_dict['created_at'], updated_at=invite_dict['created_at'],
                          is_deleted=invite_dict['is_deleted'])


def add_invite(email: str, org_id: str, member_type: MemberType) -> Invite:
    created_at = updated_at = datetime.utcnow()
    invite = Invite(email, member_type, org_id, created_at, updated_at, False, ObjectId())
    result: InsertOneResult = get_db().invites.insert_one(invite.as_dict())
    return invite


def update_or_add_invite(email: str, org_id: str, member_type: MemberType) -> Invite:
    created_at = updated_at = datetime.utcnow()
    invite = Invite(email, member_type, org_id, created_at, updated_at, False, ObjectId())
    invite_dict = invite.as_dict()

    # deleting member type and updated at since its passed in $set
    del invite_dict['member_type']
    del invite_dict['updated_at']

    get_db().invites.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({"email": invite.email, "org_id": invite.org_id},
                    {"$set": {"member_type": member_type.value, "updated_at": updated_at},
                     "$setOnInsert": invite_dict},
                    upsert=True)
    return invite


def get_invites_by_email(email: str) -> list:
    invites = []
    for invite_dict in get_db().invites.find({"email": email, "is_deleted": False}):
        invites.append(Invite.from_dict(invite_dict))
    return invites


def soft_delete_invite(invite_id: ObjectId, session) -> UpdateResult:
    updated_at = datetime.utcnow()
    result: UpdateResult = get_db().invites.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({"_id": invite_id},
                    {"$set": {"is_deleted": True,
                              "updated_at": updated_at}},
                    session=session)
    return result
