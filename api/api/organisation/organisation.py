from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.organisation import manager
from api.organisation.exceptions import *
from api.commons.organisation import OrganisationNotFoundException, DeletedOrganisationAccessException,\
    OrganisationIllegalAccessException
from api.commons.common import UnknownSystemException
from api.commons import codes


blueprint = Blueprint('organisation', __name__, url_prefix='/organisations')


@blueprint.route('', methods=['POST'])
def create_organisation():
    # does not stop you from creating multiple organisations by the same name.
    try:
        create_organisation_request = manager.OrganisationRequest(**request.json)
        create_organisation_response = manager.create_organisation(g.user_id, create_organisation_request)
        return jsonify(create_organisation_response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating organisation with given name", "code": codes.INVALID_JSON}), 400
    except OrganisationCreationException as e:
        return jsonify({"error": "Issue creating organisation due to mongo reasons",
                        "code": codes.ORGANISATION_CREATION_WRITE_EXCEPTION}), 500
    except UnknownSystemException as e:
        return jsonify({"error": "Issue with updating user details post organisation creation",
                        "code": codes.UNKNOWN_REDIS_EXCEPTION}), 500


@blueprint.route('', methods=['GET'])
def get_organisations():
    try:
        organisations = manager.get_organisations_for_user(g.user_id)
        organisations_dict = list(map(lambda org: org.dict(), organisations))
        return jsonify(organisations_dict)
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": codes.UNKNOWN_SYSTEM_EXCEPTION}), 500


@blueprint.route('/<string:org_id>', methods=['GET'])
def get_organisation(org_id: str):
    try:
        organisation: manager.GetOrganisationResponse = manager.get_organisation_for_user(org_id, g.user_id)
        return jsonify(organisation.dict())
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": codes.DELETED_ORGANISATION}), 404
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": codes.UNKNOWN_ORGANISATION}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": codes.ILLEGAL_ORGANISATION_ACCESS}), 401
    except UnknownSystemException as ex:
        return jsonify({"error": "Unknown system exception", "code": codes.UNKNOWN_SYSTEM_EXCEPTION}), 500


@blueprint.route('/<string:org_id>', methods=['PUT'])
def edit_organisation(org_id: str):
    try:
        edit_organisation_request = manager.OrganisationRequest(**request.json)
        edit_organisation_response = manager.edit_organisation(edit_organisation_request, org_id, g.user_id)
        return jsonify(edit_organisation_response.dict())
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": codes.UNKNOWN_ORGANISATION}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": codes.DELETED_ORGANISATION}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": codes.ILLEGAL_ORGANISATION_ACCESS}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": codes.UNKNOWN_SYSTEM_EXCEPTION}), 500


@blueprint.route('/<string:org_id>', methods=['DELETE'])
def delete_organisation(org_id: str):
    try:
        delete_organisation_response = manager.delete_organisation(organisation_id=org_id, user_id=g.user_id)
        return jsonify(delete_organisation_response)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": codes.UNKNOWN_ORGANISATION}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": codes.DELETED_ORGANISATION}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": codes.ILLEGAL_ORGANISATION_ACCESS}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": codes.UNKNOWN_SYSTEM_EXCEPTION}), 500
