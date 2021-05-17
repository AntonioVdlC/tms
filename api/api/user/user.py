from flask import Blueprint, current_app, request, jsonify, g
from pydantic import ValidationError

from api.user import manager
from api.user.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException, \
    OrganisationNotFoundException
from api.commons.common import UnknownSystemException
from api.commons.user import UserNotFoundException


blueprint = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


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


@blueprint.route('/email', methods=['PUT'])
def update_email():
    try:
        update_email_request = manager.UpdateEmailRequest(**request.json)
        response = manager.update_user_email(g.user_id, update_email_request)
        return jsonify(response)
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40009}), 400
    except DuplicateEmailException as e:
        return jsonify({"error": f"A user already exists for email: {e.email_id}", "code": 40010}), 400
    except DuplicateUpdateRequestException as e:
        return jsonify({"error": "User updating to another email at the moment", "code": 40011}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40441}), 404
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50016}), 500


@blueprint.route('/email/callback', methods=['PUT'])
def update_email_callback():
    try:
        email_callback_request = manager.UpdateEmailCallback(**request.json)
        response = manager.update_user_email_callback(g.user_id, email_callback_request)
        return jsonify(response)
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40012}), 400
    except UnknownEmailTypeException as e:
        return jsonify({"error": f"Request sent with illegal email type: {e.email_type}", "code": 40013}), 400
    except IllegalUpdateTokenException as e:
        current_app.logger.warn(f'Illegal update token: {e.token}')
        return jsonify({"error": f"Request sent with unknown/illegal token {e.token}. Retry if expired",
                        "code": 40014}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40442}), 404
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exception", "code": 50017}), 500


@blueprint.route('', methods=['DELETE'])
def delete_user():
    try:
        token = request.cookies.get('access_token').split()[1]
        manager.delete_user(g.user_id, token)
        response = jsonify({"message": "User deleted"})
        response.delete_cookie('access_token')
        return response
    except AttributeError as e:
        return jsonify({"message": "Missing Authorization header", "code": 40015}), 400
    except IndexError as e:
        return jsonify({"message": "Illegal token format", "code": 40016}), 400
    except SoleOwnerDeletionException as ex:
        return jsonify({"error": "Sole owner in a few organisations. Please nominate a new owner or delete org",
                        "code": 40024,
                        "organisations": ex.orgs}), 400
    except UserNotFoundException as ex:
        current_app.logger.error(f'User not found for id: {ex.user_id}')
        return jsonify({"error": f'User not found for id: {ex.user_id}', "code": 40443}), 404
    except UnknownSystemException as e:
        current_app.logger.exception('Unhandled exception', extra={'stack': True})
        return jsonify({"error": "Unknown system exception", "code": 50018}), 500
