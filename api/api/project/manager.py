from flask import current_app, g
from pydantic import BaseModel, validator
from pymongo.errors import WriteError, PyMongoError
from redis.exceptions import RedisError, ConnectionError

import json
import locale
from datetime import datetime
from typing import Optional

from api.utils.cache import get_cache
from api.project.exceptions import *
from api.models.user import User, get_user_by_id
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons
from api.commons import common as common
from api.models import project as project_db

supported_langs = set(locale.locale_alias.keys())


class ProjectRequest(BaseModel):
    project_name: str
    langs: list

    @validator('project_name')
    def validate_organisation_name(cls, v):
        if '$' in v:
            raise InvalidProjectNameException(v)
        return v

    @validator('langs')
    def validate_langs(cls, langs):
        global supported_langs
        for lang in langs:
            if lang not in supported_langs:
                raise UnsupportedLanguageException(lang)
        return langs


class ProjectModel(BaseModel):
    project_name: str
    project_id: str
    langs: list
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('project_name')
    def validate_organisation_name(cls, v):
        if '$' in v:
            raise InvalidProjectNameException(v)
        return v

    @validator('langs')
    def validate_langs(cls, langs):
        global supported_langs
        for lang in langs:
            if lang not in supported_langs:
                raise UnsupportedLanguageException(lang)
        return langs


def create_project(org_id: str, user_id: str, request: ProjectRequest) -> ProjectModel:
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

            project = project_db.add_project(request.project_name, request.langs, user_id, org_id)
            clear_projects_org_cache(org_id)
            return ProjectModel(project_name=project.name, project_id=str(project.object_id),
                                   langs=project.langs, created_at=project.created_at,
                                   updated_at=project.updated_at)
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
            filtered_projects = list(filter(lambda project: not project.is_deleted,
                                            project_db.get_projects_by_org_id(org_id)))
            response: list = list(map(lambda project: ProjectModel(project_name=project.name,
                                                                      project_id=str(project.object_id),
                                                                      langs=project.langs,
                                                                      created_at=project.created_at,
                                                                      updated_at=project.updated_at),
                                      filtered_projects))
            return response
        except (PyMongoError, RedisError) as e:
            raise common.UnknownSystemException(user_id)
    else:
        raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)


def get_project(org_id: str, user_id: str, proj_id: str) -> ProjectModel:
    organisation = organisation_commons.get_organisation_by_id(org_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

    user = user_commons.get_user(user_id)

    if str(organisation.object_id) in user.organisations:
        current_app.logger.info('user access confirmed, getting project..')
        project = get_project_for_id(proj_id)
        return ProjectModel(project_name=project.name, project_id=str(project.object_id), langs=project.langs,
                            created_at=project.created_at, updated_at=project.updated_at)
    else:
        raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)


def edit_project(org_id: str, user_id: str, proj_id: str, request: ProjectModel) -> ProjectModel:
    organisation = organisation_commons.get_organisation_by_id(org_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

    user = user_commons.get_user(user_id)
    existing_project = get_project_for_id(proj_id)

    if (str(organisation.object_id) in user.organisations) and \
            organisation_commons.check_if_admin(organisation, user_id):
        current_app.logger.info('Editing projects..')
        update_result = project_db.update_project(proj_id, request.project_name, request.langs)
        if update_result.modified_count != 1:
            raise common.UnknownSystemException(user_id)
        clear_project_cache(proj_id)
        clear_projects_org_cache(org_id)
        updated_project = get_project_for_id(proj_id)
        # TODO: if existing project and new update has different langs list, figure out to turn lang segments inactive
        return ProjectModel(project_name=updated_project.name, project_id=str(updated_project.object_id),
                            langs=updated_project.langs, created_at=updated_project.created_at,
                            updated_at=updated_project.updated_at)
    else:
        raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)


def get_projects_for_org(org_id: str) -> list:
    key = f'org_{org_id}_projects'
    cached_values = get_cache().get(key)
    if cached_values is None:
        projects = project_db.get_projects_by_org_id(org_id)
        project_dicts = list(map(lambda project: project.as_dict(to_cache=True), projects))
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(project_dicts))
        return projects
    else:
        projects = list(map(lambda project_dict: project_db.Project.from_dict(project_dict, from_cache=True),
                            json.loads(cached_values)))
        return projects


def get_project_for_id(proj_id: str) -> project_db.Project:
    key = f'project_{proj_id}'
    cached_project_str = get_cache().get(key)
    if cached_project_str is None:
        project = project_db.get_project_by_id(proj_id)
        if project is None:
            raise ProjectNotFoundExeption(proj_id)
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(project.as_dict(to_cache=True)))
    else:
        project_dict = json.loads(cached_project_str)
        project = project_db.Project.from_dict(project_dict, from_cache=True)
    return project


def clear_projects_org_cache(org_id: str):
    key = f'org_{org_id}_projects'
    get_cache().delete(key)


def clear_project_cache(proj_id: str):
    key = f'project_{proj_id}'
    get_cache().delete(key)
