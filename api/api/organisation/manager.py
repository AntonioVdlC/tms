from pydantic import BaseModel, validator
from bson.objectid import ObjectId
from pymongo.errors import WriteError, PyMongoError
from redis.exceptions import RedisError

from datetime import datetime
import json

from api.utils.cache import get_cache
from api.utils.app_wrapper import get_config, get_logger
from api.organisation.exceptions import *
from api.models.user import add_organisation_to_user, User, get_user_by_id
from api.models.organisation import *
from api.utils.db import get_client
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons
from api.commons import common as common


class OrganisationRequest(BaseModel):
    organisation_name: str

    @validator('organisation_name')
    def validate_organisation_name(cls, v):
        if '$' in v:
            raise InvalidOrgNameException(v)
        return v


class OrganisationResponse(BaseModel):
    organisation_name: str
    organisation_id: str
    created_at: datetime


class GetOrganisationResponse(BaseModel):
    organisation_name: str
    organisation_id: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


def create_organisation(user_id: str, request: OrganisationRequest) -> OrganisationResponse:
    organisation_name = str(request.organisation_name)
    user = user_commons.get_user(user_id)
    try:
        object_id = ObjectId()
        get_logger().info(f'Adding organisation with name {organisation_name} by user {user_id} with '
                          f'object id {str(object_id)}')
        with get_client().start_session() as session:
            with session.start_transaction():
                organisation = insert_organisation(organisation_name, user_id, object_id, session)
                add_organisation_to_user(user_id, str(organisation.object_id), session)
        user_commons.clear_user_cache(user_id)
    except WriteError as we:
        get_logger().error(f'issue creating organisation, org name: {organisation_name}. creator_id: {user_id}')
        raise OrganisationCreationException(organisation_name, user_id)

    response = OrganisationResponse(organisation_name=organisation.name,
                                    organisation_id=str(organisation.object_id),
                                    created_at=organisation.created_at)
    return response


def get_organisations_for_user(user_id: str) -> list:
    try:
        user = user_commons.get_user(user_id)
        if len(user.organisations) > 0:
            organisations = list(filter(lambda org: not org.is_deleted, get_organisations_by_ids(user.organisations)))
            response: list = \
                list(map(lambda organisation: GetOrganisationResponse(organisation_name=organisation.name,
                                                                      organisation_id=str(organisation.object_id),
                                                                      created_at=organisation.created_at,
                                                                      updated_at=organisation.updated_at,
                                                                      is_deleted=organisation.is_deleted),
                         organisations))
            return response
        else:
            return []
    except (PyMongoError, RedisError) as e:
        raise common.UnknownSystemException(user_id)


def get_organisation_for_user(organisation_id: str, user_id: str) -> GetOrganisationResponse:
    organisation = organisation_commons.get_organisation_by_id(organisation_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=organisation_id)

    user = user_commons.get_user(user_id)

    if organisation_id in user.organisations:
        get_logger().info('User has access to organisation..')
        response: GetOrganisationResponse = GetOrganisationResponse(organisation_name=organisation.name,
                                                                    organisation_id=str(organisation.object_id),
                                                                    created_at=organisation.created_at,
                                                                    updated_at=organisation.updated_at,
                                                                    is_deleted=organisation.is_deleted)
        return response
    else:
        raise organisation_commons.OrganisationIllegalAccessException(organisation_id, user_id)


def edit_organisation(request: OrganisationRequest, organisation_id: str, user_id: str) -> OrganisationResponse:
    organisation = organisation_commons.get_organisation_by_id(organisation_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=organisation_id)

    user = user_commons.get_user(user_id)

    if (str(organisation.object_id) in user.organisations) and \
            organisation_commons.check_if_admin(organisation, user_id):
        get_logger().info('Editing organisation..')
        update_result = update_organisation(organisation_id, request.organisation_name)
        if update_result.modified_count != 1:
            raise common.UnknownSystemException(user_id)
        organisation_commons.clear_org_cache(organisation_id)
        organisation = organisation_commons.get_organisation_by_id(organisation_id)
        return OrganisationResponse(organisation_name=organisation.name,
                                    organisation_id=str(organisation.object_id),
                                    created_at=organisation.created_at)
    else:
        raise organisation_commons.OrganisationIllegalAccessException(organisation_id, user_id)


def delete_organisation(organisation_id: str, user_id: str):
    organisation = organisation_commons.get_organisation_by_id(organisation_id)
    if organisation.is_deleted:
        raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=organisation_id)

    user = user_commons.get_user(user_id)

    if (str(organisation.object_id) in user.organisations) and \
            organisation_commons.check_if_admin(organisation, user_id):
        get_logger().info('Deleting organisation..')
        delete_result = soft_delete_organisation(organisation_id)
        if delete_result.modified_count != 1:
            raise common.UnknownSystemException(user_id)
        organisation_commons.clear_org_cache(organisation_id)
        return {"message": "organisation deleted"}
    else:
        raise organisation_commons.OrganisationIllegalAccessException(organisation_id, user_id)


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
        pipeline.setex(key, get_config()['CACHE_TTL_SECS'],
                       json.dumps(uncached_organisation.as_dict(to_cache=True)))
    pipeline.execute()
    organisations = cached_organisations + uncached_organisations
    return organisations

