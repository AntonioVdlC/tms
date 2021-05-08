from pydantic import BaseModel, validator, EmailStr
from pymongo.errors import PyMongoError, WriteError
from bson.objectid import ObjectId
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


class MemberModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    member_type: organisation_commons.MemberType
    added_at: datetime
    updated_at: datetime
    is_deleted: bool


class InviteModel(BaseModel):
    id: str
    email: EmailStr
    member_type: organisation_commons.MemberType
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


class AddMemberRequest(BaseModel):
    email: EmailStr
    member_type: organisation_commons.MemberType


class EditMemberRequest(BaseModel):
    member_type: organisation_commons.MemberType


class EditInviteRequest(BaseModel):
    email: EmailStr
    member_type: organisation_commons.MemberType


class EditInviteResponse(BaseModel):
    soft_deleted: bool
    invite: InviteModel


def add_member(org_id: str, user_id: str, request: AddMemberRequest):
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)

        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin_and_above(organisation, user_id):
            if request.member_type == organisation_db.MemberType.owner and not \
                    organisation_commons.check_if_owner(organisation, user_id):
                raise InsufficientOwnerAccessException(user_id)

            member_email = str(request.email)
            existing_member: user_db.User = user_db.get_user_by_email(member_email)
            if existing_member is None:
                get_logger().info('Member not present.. creating an invite entry for later resolution')
                invite_db.update_or_add_invite(member_email, org_id, request.member_type)
                # TODO: keep a counter on member email to organisation so they aren't spammed
                send_member_signup_email(member_email, organisation.name)
                return {"message": "Member requested to signup"}
            else:
                get_logger().info('Member present.. proceeding to add to organisation')
                member_ids = list(map(lambda member: member.user_id, organisation.members))
                if str(existing_member.object_id) in member_ids:
                    get_logger().warn('User already in members list..')
                    raise DuplicateAddMemberException(existing_member.email,
                                                      existing_member.first_name,
                                                      existing_member.last_name)
                else:
                    with get_client().start_session() as session:
                        with session.start_transaction():
                            user_db.add_organisations_to_user(str(existing_member.object_id), [org_id], session)
                            organisation_db.add_member_to_organisation(org_id,
                                                                       str(existing_member.object_id),
                                                                       request.member_type,
                                                                       session)
                    organisation_commons.clear_org_cache(org_id)
                    return {"message": "Member added to organisation and notified"}
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        get_logger().exception("error ", extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def edit_member(org_id: str, user_id: str, member_id: str, request: EditMemberRequest) -> MemberModel:
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)

        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin_and_above(organisation, user_id):
            if request.member_type == organisation_db.MemberType.owner and not \
                    organisation_commons.check_if_owner(organisation, user_id):
                raise InsufficientOwnerAccessException(user_id)
            member_ids = list(map(lambda m: m.member_id, organisation.members))
            if member_id not in member_ids:
                raise UnknownMemberException(member_id)

            update_result = organisation_db.edit_member(org_id, member_id, request.member_type)
            if update_result.modified_count != 1:
                raise common.UnknownSystemException(user_id)
            organisation_commons.clear_org_cache(org_id)
            member = organisation_db.get_member(org_id, member_id)
            member_details = user_commons.get_user(member.user_id)
            return MemberModel(id=member.member_id, first_name=member_details.first_name,
                               last_name=member_details.last_name, member_type=member.member_type,
                               added_at=member.added_at, updated_at=member.updated_at, is_deleted=member.is_deleted)
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        get_logger().exception("error ", extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def edit_invite(org_id: str, user_id: str, invite_id: str, request: EditInviteRequest) -> EditInviteResponse:
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)

        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin_and_above(organisation, user_id):
            if request.member_type == organisation_db.MemberType.owner and not \
                    organisation_commons.check_if_owner(organisation, user_id):
                raise InsufficientOwnerAccessException(user_id)
            member_email = str(request.email)
            existing_member: user_db.User = user_db.get_user_by_email(member_email)
            soft_deleted = False
            if existing_member is None:
                get_logger().info('No existing member, proceeding to update invite')
                update_result = invite_db.edit_invite(invite_id, str(request.email), request.member_type)
                if update_result.modified_count != 1:
                    raise common.UnknownSystemException(user_id)
            else:
                get_logger().info('Member present.. proceeding to add to organisation')
                member_ids = list(map(lambda member: member.user_id, organisation.members))
                if str(existing_member.object_id) in member_ids:
                    get_logger().warn('User already in members list..')
                    raise DuplicateAddMemberException(existing_member.email,
                                                      existing_member.first_name,
                                                      existing_member.last_name)
                else:
                    with get_client().start_session() as session:
                        with session.start_transaction():
                            user_db.add_organisations_to_user(str(existing_member.object_id), [org_id], session)
                            organisation_db.add_member_to_organisation(org_id,
                                                                       str(existing_member.object_id),
                                                                       request.member_type,
                                                                       session)
                            invite_db.edit_invite_and_soft_delete(invite_id, str(request.email),
                                                                  request.member_type, session)
                    organisation_commons.clear_org_cache(org_id)
                    soft_deleted = True
            new_invite = invite_db.get_invite(invite_id)
            if new_invite is None:
                raise common.UnknownSystemException(user_id)
            else:
                invite_model = InviteModel(id=str(new_invite.object_id), email=new_invite.email,
                                           member_type=new_invite.member_type, created_at=new_invite.created_at,
                                           updated_at=new_invite.updated_at, is_deleted=new_invite.is_deleted)
                return EditInviteResponse(soft_deleted=soft_deleted, invite=invite_model)
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        get_logger().exception("error ", extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def get_members(org_id: str, user_id: str) -> list:
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)
        if str(organisation.object_id) in user.organisations:
            user_ids = list(map(lambda member: member.user_id, organisation.members))
            users_dict = user_commons.get_user_by_ids(user_ids)
            response = list(map(lambda member: MemberModel(id=member.member_id,
                                                           first_name=users_dict[member.user_id].first_name,
                                                           last_name=users_dict[member.user_id].last_name,
                                                           member_type=member.member_type,
                                                           added_at=member.added_at, updated_at=member.updated_at,
                                                           is_deleted=member.is_deleted),
                                organisation.members))
            return response
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        get_logger().exception("error", extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def get_invites(org_id: str, user_id: str) -> list:
    try:
        organisation = organisation_commons.get_organisation_by_id(org_id)
        if organisation.is_deleted:
            raise organisation_commons.DeletedOrganisationAccessException(user_id=user_id, org_id=org_id)

        user = user_commons.get_user(user_id)
        if (str(organisation.object_id) in user.organisations) and \
                organisation_commons.check_if_admin_and_above(organisation, user_id):
            invites = invite_db.get_invites_by_org(org_id)
            response = list(map(lambda invite: InviteModel(id=str(invite.object_id), email=invite.email,
                                                           member_type=invite.member_type, created_at=invite.created_at,
                                                           updated_at=invite.updated_at, is_deleted=invite.is_deleted),
                                invites))
            return response
        else:
            raise organisation_commons.OrganisationIllegalAccessException(org_id, user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        get_logger().exception("error", extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def add_member_to_organisation(existing_member: user_db.User,
                               member_type: organisation_db.MemberType,
                               organisation: organisation_db.Organisation):
    get_logger().info('Member present.. proceeding to add to organisation')
    org_id = str(organisation.object_id)
    member_ids = list(map(lambda member: member.user_id, organisation.members))
    if str(existing_member.object_id) in member_ids:
        get_logger().warn('User already in members list..')
        return {"message": "User already in members list"}
    else:
        with get_client().start_session() as session:
            with session.start_transaction():
                user_db.add_organisations_to_user(str(existing_member.object_id), [org_id], session)
                organisation_db.add_member_to_organisation(org_id,
                                                           str(existing_member.object_id),
                                                           member_type,
                                                           session)
        organisation_commons.clear_org_cache(org_id)


def send_member_signup_email(email: str, org_name: str):
    get_logger().info('Sending signup email to member..')
    # TODO: antonio, email.


def send_member_added_email(email: str, org_name: str):
    get_logger().info('Sending signup email to member..')
    # TODO: antonio, email
