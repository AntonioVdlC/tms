from flask import current_app, g
from pydantic import BaseModel, validator
from bson.objectid import ObjectId
from pymongo.errors import WriteError, PyMongoError
from redis.exceptions import RedisError

from datetime import datetime
import json

from api.utils.cache import get_cache
from api.organisation.exceptions import *
from api.models.user import add_organisation_to_user, User, get_user_by_id
from api.models.organisation import insert_organisation, Organisation, get_organisation, get_organisations
from api.utils.db import get_client


class CreateOrganisationRequest(BaseModel):
    organisation_name: str

    @validator('organisation_name')
    def validate_organisation_name(cls, v):
        if '$' in v:
            raise InvalidOrgNameException(v)
        return v


class CreateOrganisationResponse(BaseModel):
    organisation_name: str
    organisation_id: str
    created_at: datetime


def create_organisation(request: CreateOrganisationRequest) -> CreateOrganisationResponse:
    organisation_name = str(request.organisation_name)
    try:
        object_id = ObjectId()
        current_app.logger.info(f'Adding organisation with name {organisation_name} by user {g.user_id} with '
                                f'object id {str(object_id)}')
        with get_client().start_session() as session:
            with session.start_transaction():
                organisation = insert_organisation(organisation_name, g.user_id, object_id, session)
                add_organisation_to_user(g.user_id, str(organisation.object_id), session)
        clear_user_cache(g.user_id)
    except WriteError as we:
        current_app.logger.error(f'issue creating organisation, org name: {organisation_name}. creator_id: {g.user_id}')
        raise OrganisationCreationException(organisation_name, g.user_id)

    response = CreateOrganisationResponse(organisation_name=organisation.name,
                                          organisation_id=str(organisation.object_id),
                                          created_at=organisation.created_at)
    return response


def get_organisations_for_user(user_id: str):
    try:
        user = get_user(user_id)
        organisations = get_organisations_by_ids(user.organisations)
        organisations_dict = list(map(lambda org: org.as_dict(to_cache=True), organisations))
        return organisations_dict
    except (PyMongoError, RedisError) as e:
        raise UnknownSystemException(user_id)


def get_organisation_for_user(organisation_id: str, user_id: str) -> Organisation:
    user = get_user(user_id)
    organisation = get_organisation_by_id(organisation_id)
    if organisation_id in user.organisations:
        current_app.logger.info('User has access to organisation..')
        return organisation.as_dict(to_cache=True)
    else:
        raise OrganisationIllegalAccessException(organisation_id, user_id)


def get_user(user_id: str) -> User:
    key = f'user_{user_id}'
    cached_user_str = get_cache().get(key)
    user: User = None
    if cached_user_str is None:
        user = get_user_by_id(user_id)
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(user.as_dict(to_cache=True)))
    else:
        user_dict = json.loads(cached_user_str)
        user = User.from_dict(user_dict, from_cache=True)
    return user


def get_organisations_by_ids(org_ids: list):
    keys = list(map(lambda organisation_id: f'org_{organisation_id}', org_ids))
    cached_organisation_str_list = [x for x in get_cache().mget(*keys) if x is not None]
    cached_organisations = list(map(lambda organisation_str: Organisation.from_dict(json.loads(organisation_str),
                                                                                    from_cache=True),
                                    cached_organisation_str_list))
    un_cached_org_ids = []
    cached_org_ids = list(map(lambda organisation: str(organisation.object_id), cached_organisations))
    for org_id in org_ids:
        if org_id not in cached_org_ids:
            un_cached_org_ids.append(org_id)
    uncached_organisations = get_organisations(un_cached_org_ids)
    pipeline = get_cache().pipeline()
    for uncached_organisation in uncached_organisations:
        key = f'org_{str(uncached_organisation.object_id)}'
        pipeline.setex(key, current_app.config['CACHE_TTL_SECS'],
                       json.dumps(uncached_organisation.as_dict(to_cache=True)))
    pipeline.execute()
    organisations = cached_organisations + uncached_organisations
    return organisations


def get_organisation_by_id(org_id: str) -> Organisation:
    key = f'org_{org_id}'
    cached_org_str = get_cache().get(key)
    organisation: Organisation = None
    if cached_org_str is None:
        organisation = get_organisation(org_id)
        if organisation is None:
            raise OrganisationNotFoundException(org_id)
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(organisation.as_dict(to_cache=True)))
    else:
        org_dict = json.loads(cached_org_str)
        organisation = Organisation.from_dict(org_dict, from_cache=True)
    return organisation


def clear_user_cache(user_id: str):
    key = f'user_{user_id}'
    get_cache().delete(key)
