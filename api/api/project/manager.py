from flask import current_app, g
from pydantic import BaseModel, validator
from pymongo.errors import WriteError, PyMongoError
from redis.exceptions import RedisError, ConnectionError

import json
import locale
from datetime import datetime

from api.utils.cache import get_cache
from api.project.exceptions import *
from api.models.user import User, get_user_by_id
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons
from api.commons import common as common
from api.models.project import *

supported_langs = set(locale.locale_alias.keys())


class ProjectRequest(BaseModel):
    project_name: str
    langs: list

    @validator('langs')
    def validate_langs(cls, langs):
        global supported_langs
        for lang in langs:
            if lang not in supported_langs:
                raise UnsupportedLanguageException(lang)
        return langs


class ProjectResponse(BaseModel):
    project_name: str
    project_id: str
    langs: list
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


def create_project(org_id: str, user_id: str, request: ProjectRequest) -> ProjectResponse:
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)

        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin(organisation, user_id):
            existing_project_names = list(map(lambda p: p.name, get_projects_for_org(org_id)))
            if request.project_name.strip() in existing_project_names:
                raise DuplicateProjectNameException(request.project_name)

            project = add_project(request.project_name, request.langs, user_id, org_id)
            clear_projects_org_cache(org_id)
            return ProjectResponse(project_name=project.name, project_id=str(project.object_id),
                                   langs=project.langs, created_at=project.created_at,
                                   updated_at=project.updated_at, is_deleted=project.is_deleted)
        else:
            organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        raise common.UnknownSystemException(user_id)


def get_projects(org_id: str, user_id: str) -> list:
    organisation = organisation_commons.get_organisation_by_id(org_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

    user = user_commons.get_user(user_id)

    if str(organisation.object_id) in user.organisations:
        try:
            filtered_projects = list(filter(lambda project: not project.is_deleted, get_projects_by_org_id(org_id)))
            response: list = list(map(lambda project: ProjectResponse(project_name=project.name,
                                                                      project_id=str(project.object_id),
                                                                      langs=project.langs,
                                                                      created_at=project.created_at,
                                                                      updated_at=project.updated_at,
                                                                      is_deleted=project.is_deleted),
                                      filtered_projects))
            return response
        except (PyMongoError, RedisError) as e:
            raise common.UnknownSystemException(user_id)
    else:
        raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)


def get_projects_for_org(org_id: str) -> list:
    key = f'org_{org_id}_projects'
    cached_values = get_cache().get(key)
    if cached_values is None:
        projects = get_projects_by_org_id(org_id)
        project_dicts = list(map(lambda project: project.as_dict(to_cache=True), projects))
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(project_dicts))
        return projects
    else:
        projects = list(map(lambda project_dict: Project.from_dict(project_dict, from_cache=True),
                            json.loads(cached_values)))
        return projects


def clear_projects_org_cache(org_id: str):
    key = f'org_{org_id}_projects'
    get_cache().delete(key)
