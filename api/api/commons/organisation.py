from flask import current_app

import json

from api.models.organisation import get_organisation, Organisation, MemberType
from api.utils.cache import get_cache


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


def check_if_admin(organisation, user_id) -> bool:
    flag = False
    for member in organisation.members:
        if (member.user_id == user_id) and (member.member_type == MemberType.admin):
            flag = True
            break
    return flag


def clear_org_cache(org_id: str):
    key = f'org_{org_id}'
    get_cache().delete(key)
