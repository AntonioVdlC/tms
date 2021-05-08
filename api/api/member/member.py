from flask import Blueprint, current_app, request, jsonify, g
from pydantic import ValidationError

from api.member import manager
from api.member.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException, \
    OrganisationNotFoundException
from api.commons.common import UnknownSystemException
from api.commons.user import UserNotFoundException


blueprint = Blueprint('member', __name__, url_prefix='/organisations/<string:org_id>/members')


@blueprint.route('', methods=['PUT'])
def add_member(org_id: str):
    try:
        add_member_request = manager.AddMemberRequest(**request.json)
        response = manager.add_member(org_id, g.user_id, add_member_request)
        return jsonify(response)
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40016}), 400
    except DuplicateAddMemberException as ex:
        current_app.logger.error(f'Already member in list for email: {ex.email}. Please delete invite if not needed')
        return jsonify({"error": f'Already member in list for email: {ex.email}. Please delete invite if not needed',
                        "code": 40017}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40444}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40445}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40446}), 404
    except InsufficientOwnerAccessException as ex:
        current_app.logger.warn(f'Trying to add owner with insufficient permission: {ex.user_id}')
        return jsonify({"error": "Only an owner can add another owner", "code": 40114}), 401
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40115}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50014}), 500


@blueprint.route('', methods=['GET'])
def get_members(org_id: str):
    try:
        response = list(map(lambda member: member.dict(), manager.get_members(org_id, g.user_id)))
        return jsonify(response)
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40447}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40448}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40449}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40116}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50015}), 500


@blueprint.route('/invites', methods=['GET'])
def get_invites(org_id: str):
    try:
        response = list(map(lambda invite: invite.dict(), manager.get_invites(org_id, g.user_id)))
        return jsonify(response)
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40450}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40451}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40452}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40117}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50016}), 500


@blueprint.route('/<string:member_id>', methods=['PUT'])
def edit_member(org_id: str, member_id: str):
    try:
        edit_member_request = manager.EditMemberRequest(**request.json)
        response = manager.edit_member(org_id, g.user_id, member_id, edit_member_request)
        return jsonify(response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40018}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40453}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40454}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40455}), 404
    except UnknownMemberException as ex:
        current_app.logger.warn(f'Unknown member id: {ex.member_id}')
        return jsonify({"error": f"Unknown member id: {ex.member_id}", "code": 40456}), 404
    except InsufficientOwnerAccessException as ex:
        current_app.logger.warn(f'Trying to add owner with insufficient permission: {ex.user_id}')
        return jsonify({"error": "Only an owner can add another owner", "code": 40117}), 401
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40118}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50015}), 500


@blueprint.route('/invites/<string:invite_id>', methods=['PUT'])
def edit_invite(org_id: str, invite_id: str):
    try:
        edit_invite_request = manager.EditInviteRequest(**request.json)
        response = manager.edit_invite(org_id, g.user_id, invite_id, edit_invite_request)
        return jsonify(response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40019}), 400
    except DuplicateAddMemberException as ex:
        current_app.logger.error(f'Already member in list for email: {ex.email}. Please delete invite if not needed')
        return jsonify({"error": f'Already member in list for email: {ex.email}. Please delete invite if not needed',
                        "code": 40020}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40456}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40457}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40458}), 404
    except InsufficientOwnerAccessException as ex:
        current_app.logger.warn(f'Trying to add owner with insufficient permission: {ex.user_id}')
        return jsonify({"error": "Only an owner can add another owner", "code": 40119}), 401
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40120}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50016}), 500


@blueprint.route('/<string:member_id>', methods=['DELETE'])
def delete_member(org_id: str, member_id: str):
    try:
        response = manager.delete_member(org_id, g.user_id, member_id)
        return jsonify(response)
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40459}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40460}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40461}), 404
    except UnknownMemberException as ex:
        current_app.logger.warn(f"unknown member id: {ex.member_id}")
        return jsonify({"error": f"Unknown member id: {ex.member_id}", "code": 40021}), 400
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "Not enough permissions to perform action", "code": 40121}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50017}), 500

