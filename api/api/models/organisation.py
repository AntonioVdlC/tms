from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.write_concern import WriteConcern

from datetime import datetime
from enum import Enum

from api.utils.db import get_db


class MemberType(str, Enum):
    owner = 'owner'
    admin = 'admin'
    developer = 'developer'
    translator = 'translator'


class Member(object):
    def __init__(self, member_id: str, user_id: str, member_type: MemberType, added_at: datetime, updated_at: datetime,
                 is_deleted: bool = False):
        self.member_id = member_id
        self.user_id = user_id
        self.member_type = member_type
        self.added_at = added_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted

    def as_dict(self, to_cache=False):
        if to_cache:
            return {"id": self.member_id, "user_id": self.user_id, "member_type": self.member_type.value,
                    "added_at": self.added_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f'), "is_deleted": self.is_deleted}
        else:
            return {"id": self.member_id, "user_id": self.user_id, "member_type": self.member_type.value,
                    "added_at": self.added_at, "updated_at": self.updated_at, "is_deleted": self.is_deleted}

    @staticmethod
    def from_dict(member_dict, from_cache=False):
        if from_cache:
            return Member(member_id=member_dict['id'], user_id=member_dict['user_id'],
                          member_type=MemberType[member_dict['member_type']],
                          added_at=datetime.strptime(member_dict['added_at'], '%Y-%m-%d %H:%M:%S.%f'),
                          updated_at=datetime.strptime(member_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f'),
                          is_deleted=member_dict['is_deleted'])
        else:
            return Member(member_id=member_dict['id'], user_id=member_dict['user_id'],
                          member_type=MemberType[member_dict['member_type']], added_at=member_dict['added_at'],
                          updated_at=member_dict['updated_at'], is_deleted=member_dict['is_deleted'])


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

    def as_dict(self, to_cache=False):
        members_list = list(map(lambda member: member.as_dict(to_cache=to_cache), self.members))
        organisation_dict = {"name": self.name, "members": members_list, "creator_id": self.creator_id,
                             "is_deleted": self.is_deleted}
        if to_cache:
            organisation_dict['_id'] = str(self.object_id)
            organisation_dict['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            organisation_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            organisation_dict['_id'] = self.object_id
            organisation_dict['created_at'] = self.created_at
            organisation_dict['updated_at'] = self.updated_at
        return organisation_dict

    @staticmethod
    def from_dict(organisation_dict, from_cache=False):
        members = list(map(lambda member_dict: Member.from_dict(member_dict, from_cache),
                           organisation_dict['members']))
        if from_cache:
            object_id = ObjectId(organisation_dict['_id'])
            created_at = datetime.strptime(organisation_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            updated_at = datetime.strptime(organisation_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
            return Organisation(object_id=object_id, name=organisation_dict['name'], members=members,
                                creator_id=organisation_dict['creator_id'], is_deleted=organisation_dict['is_deleted'],
                                created_at=created_at, updated_at=updated_at)
        else:
            return Organisation(object_id=organisation_dict['_id'], name=organisation_dict['name'], members=members,
                                creator_id=organisation_dict['creator_id'], is_deleted=organisation_dict['is_deleted'],
                                created_at=organisation_dict['created_at'], updated_at=organisation_dict['updated_at'])


def insert_organisation(name: str, creator_id: str, object_id: ObjectId, session):
    created_at = updated_at = added_at = datetime.utcnow()
    member_id = str(ObjectId())
    members = [Member(member_id, creator_id, MemberType.owner, added_at, updated_at)]
    organisation = Organisation(name, members, creator_id, created_at, updated_at, False, object_id)
    result: InsertOneResult = get_db().organisations.insert_one(organisation.as_dict(), session=session)
    return organisation


def get_organisation(object_id: str) -> Organisation:
    org_dict = get_db().organisations.find_one({"_id": ObjectId(object_id), "is_deleted": False})
    if org_dict is None:
        return None
    else:
        return Organisation.from_dict(org_dict)


def get_organisations(object_ids: list) -> list:
    ids = list(map(lambda object_id: ObjectId(object_id), object_ids))
    organisations = []
    for org_dict in get_db().organisations.find({"_id": {"$in": ids}, "is_deleted": False}):
        organisations.append(Organisation.from_dict(org_dict))
    return organisations


def update_organisation(org_id: str, name: str) -> UpdateResult:
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority")) \
            .update_one({"_id": ObjectId(org_id)},
                        {'$set': {'name': name,
                                  'updated_at': datetime.utcnow()}},
                        upsert=False)
    return result


def add_member_to_organisation(org_id: str, user_id: str, member_type: MemberType, session):
    updated_at = added_at = datetime.utcnow()
    member_id = str(ObjectId())
    member = Member(member_id=member_id, user_id=user_id, member_type=member_type,
                    added_at=added_at, updated_at=updated_at)
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(org_id)},
                    {'$addToSet': {'members': member.as_dict()},
                     '$set': {'updated_at': updated_at}},
                    upsert=False,
                    session=session)
    return result


def edit_member(org_id: str, member_id: str, member_type: MemberType) -> UpdateResult:
    updated_at = datetime.utcnow()
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(org_id), 'members.id': member_id},
                    {'$set': {'members.$.member_type': member_type.value,
                              'members.$.updated_at': updated_at,
                              'updated_at': updated_at}},
                    upsert=False)
    return result


def soft_delete_member(org_id: str, member_id: str, session) -> UpdateResult:
    updated_at = datetime.utcnow()
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(org_id), 'members.id': member_id},
                    {'$set': {'members.$.is_deleted': True,
                              'members.$.updated_at': updated_at,
                              'updated_at': updated_at}},
                    session=session,
                    upsert=False)
    return result


def enable_deleted_member(org_id: str, member_id: str, session) -> UpdateResult:
    updated_at = datetime.utcnow()
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({'_id': ObjectId(org_id), 'members.id': member_id},
                    {'$set': {'members.$.is_deleted': False,
                              'members.$.updated_at': updated_at,
                              'updated_at': updated_at}},
                    session=session,
                    upsert=False)
    return result


def get_member(org_id: str, member_id: str) -> Member:
    members = get_db().organisations.find_one({"_id": ObjectId(org_id),
                                               "members": {"$elemMatch": {"id": member_id}}},
                                              {"members.$": 1})['members']
    if len(members) == 0:
        return None
    else:
        member_dict = members[0]
        return Member.from_dict(member_dict)


def soft_delete_organisation(org_id: str) -> UpdateResult:
    result: UpdateResult = get_db().organisations.with_options(write_concern=WriteConcern(w="majority"))\
        .update_one({"_id": ObjectId(org_id)},
                    {'$set': {'is_deleted': True}},
                    upsert=False)
    return result
