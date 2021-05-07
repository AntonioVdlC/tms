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
def get_members(org_id: str):
    try:
        add_member_request = manager.AddMemberRequest(**request.json)
        response = manager.add_member(org_id, g.user_id, add_member_request)
        return jsonify(response)
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40016}), 400
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
