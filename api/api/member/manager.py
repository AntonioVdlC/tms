from pydantic import BaseModel, validator, EmailStr
from pymongo.errors import PyMongoError, WriteError
from redis.exceptions import RedisError, ConnectionError

import json
from datetime import datetime

from api.utils.cache import get_cache
from api.utils.app_wrapper import get_config, get_logger
from api.member.exceptions import *
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons
from api.commons import common as common
from api.models import user as user_db
from api.models import organisation as organisation_db
from api.models import invite as invite_db
from api.utils.db import get_client


class MemberModel:
    id: str
    member_type: organisation_commons.MemberType
    added_at: datetime
    updated_at: datetime
    is_deleted: bool


class AddMemberRequest(BaseModel):
    email: EmailStr
    member_type: organisation_commons.MemberType


def add_member(org_id: str, user_id: str, request: AddMemberRequest):
    try:
        get_logger().info('Adding member..')
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)

        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin_and_above(organisation, user_id):
            member_email = str(request.email)
            existing_member = user_db.get_user_by_email(member_email)
            if existing_member is None:
                get_logger().info('Member not present.. creating an invite entry for later resolution')
                invite_db.add_invite(member_email, org_id, request.member_type)
                send_member_signup_email(member_email, organisation.name)
                return {"message": "Member requested to signup"}
            else:
                get_logger().info('Member present.. proceeding to add to organisation')
                with get_client().start_session() as session:
                    with session.start_transaction():
                        user_db.add_organisation_to_user(str(existing_member.object_id), org_id, session)
                        organisation_db.add_member_to_organisation(org_id,
                                                                   str(existing_member.object_id),
                                                                   request.member_type,
                                                                   session)
                return {"message": "Member added to organisation and notified"}
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        raise common.UnknownSystemException(user_id)


def send_member_signup_email(email: str, org_name: str):
    get_logger().info('Sending signup email to member..')
    # TODO: antonio, email.


def send_member_added_email(email: str, org_name: str):
    get_logger().info('Sending signup email to member..')
    # TODO: antonio, email
