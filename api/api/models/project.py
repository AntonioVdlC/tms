from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.write_concern import WriteConcern

from datetime import datetime

from api.utils.db import get_db


class Project(object):
    def __init__(self, name: str, langs: list, creator_id: str, org_id: str, created_at: datetime, updated_at: datetime,
                 is_deleted: bool, object_id: ObjectId, key: list = []):
        self.object_id = object_id
        self.name = name
        self.langs = langs
        self.creator_id = creator_id
        self.org_id = org_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted
        self.key = key

    def as_dict(self, to_cache=False):
        project_dict = {"name": self.name, "langs": self.langs, "creator_id": self.creator_id, "org_id": self.org_id,
                        "is_deleted": self.is_deleted, "key": self.key}
        if to_cache:
            project_dict['_id'] = str(self.object_id)
            project_dict['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            project_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            project_dict['_id'] = self.object_id
            project_dict['created_at'] = self.created_at
            project_dict['updated_at'] = self.updated_at
        return project_dict

    @staticmethod
    def from_dict(project_dict, from_cache=False):
        if from_cache:
            object_id = ObjectId(project_dict['_id'])
            created_at = datetime.strptime(project_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            updated_at = datetime.strptime(project_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
            return Project(object_id=object_id, name=project_dict['name'], langs=project_dict['langs'],
                           creator_id=project_dict['creator_id'], org_id=project_dict['org_id'],
                           is_deleted=project_dict['is_deleted'], key=project_dict['key'],
                           created_at=created_at, updated_at=updated_at)
        else:
            return Project(object_id=project_dict['_id'], name=project_dict['name'], langs=project_dict['langs'],
                           creator_id=project_dict['creator_id'], org_id=project_dict['org_id'],
                           is_deleted=project_dict['is_deleted'], key=project_dict['key'],
                           created_at=project_dict['created_at'], updated_at=project_dict['updated_at'])


def add_project(name: str, langs: list, creator_id: str, org_id: str) -> Project:
    created_at = updated_at = datetime.utcnow()
    project = Project(name=name, langs=langs, creator_id=creator_id, org_id=org_id, updated_at=updated_at,
                      created_at=created_at, is_deleted=False, object_id=ObjectId())
    get_db().projects.insert_one(project.as_dict())
    return project


def get_projects_by_org_id(org_id: str) -> list:
    projects = []
    for project_dict in get_db().projects.find({"org_id": org_id, "is_deleted": False}):
        projects.append(Project.from_dict(project_dict))
    return projects


def get_project_by_id(object_id: str) -> Project:
    proj_dict = get_db().projects.find_one({"_id": ObjectId(object_id), "is_deleted": False})
    if proj_dict is None:
        return None
    else:
        return Project.from_dict(proj_dict)


def update_project(proj_id: str, name: str, langs: list) -> UpdateResult:
    result: UpdateResult = get_db().projects.with_options(write_concern=WriteConcern(w="majority"))\
                                            .update_one({"_id": ObjectId(proj_id)},
                                                        {'$set': {'name': name,
                                                                  'langs': langs,
                                                                  'updated_at': datetime.utcnow()}},
                                                        upsert=False)
    return result


def soft_delete_project(proj_id: str) -> UpdateResult:
    result: UpdateResult = get_db().projects.with_options(write_concern=WriteConcern(w="majority")) \
                                    .update_one({"_id": ObjectId(proj_id)},
                                                {'$set': {'is_deleted': True}},
                                                upsert=False)
    return result
