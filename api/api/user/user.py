from flask import Blueprint, current_app, request, jsonify, g
from pydantic import ValidationError

from api.user import manager
from api.user.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException, \
    OrganisationNotFoundException
from api.commons.common import UnknownSystemException
from api.commons.user import UserNotFoundException


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('', methods=['GET'])
def get_user():
    try:
        response = manager.get_user(g.user_id)
        return jsonify(response.dict())
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40439}), 404
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50014}), 500


@blueprint.route('/details', methods=['PUT'])
def update_details():
    try:
        update_details_request = manager.UpdateDetailsRequest(**request.json)
        response = manager.update_user_details(g.user_id, update_details_request)
        return response.dict()
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40008}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40440}), 404
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50015}), 500
