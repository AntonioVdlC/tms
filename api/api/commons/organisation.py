from flask import current_app

import json

from api.models.organisation import get_organisation, Organisation, MemberType, get_organisations
from api.utils.cache import get_cache
from api.utils.app_wrapper import get_config


class OrganisationNotFoundException(Exception):
    def __init__(self, org_id):
        self.org_id = org_id


class DeletedOrganisationAccessException(Exception):
    def __init__(self, user_id, org_id):
        self.user_id = user_id
        self.org_id = org_id


class OrganisationIllegalAccessException(Exception):
    def __init__(self, org_id, user_id):
        self.org_id = org_id
        self.user_id = user_id


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


def check_if_admin_and_above(organisation, user_id) -> bool:
    flag = False
    for member in organisation.members:
        if (member.user_id == user_id) and (member.member_type == MemberType.owner or
                                            member.member_type == MemberType.admin):
            flag = True
            break
    return flag


def check_if_owner(organisation, user_id) -> bool:
    flag = False
    for member in organisation.members:
        if (member.user_id == user_id) and (member.member_type == MemberType.owner):
            flag = True
            break
    return flag


def check_if_dev_and_above(organisation, user_id) -> bool:
    flag = False
    for member in organisation.members:
        if (member.user_id == user_id) and (member.member_type == MemberType.admin or
                                            member.member_type == MemberType.developer):
            flag = True
            break
    return flag


def clear_org_cache(org_id: str):
    key = f'org_{org_id}'
    get_cache().delete(key)


def clear_orgs_cache(org_ids: list):
    keys = list(map(lambda org_id: f'org_{org_id}', org_ids))
    get_cache().delete(*keys)
