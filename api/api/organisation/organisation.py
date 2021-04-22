from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.organisation import manager
from api.organisation.exceptions import *


blueprint = Blueprint('organisation', __name__, url_prefix='/organisations')


@blueprint.route('', methods=['POST'])
def create_organisation():
    # does not stop you from creating multiple organisations by the same name.
    try:
        create_organisation_request = manager.CreateOrganisationRequest(**request.json)
        create_organisation_response = manager.create_organisation(create_organisation_request)
        return jsonify(create_organisation_response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating organisation with given name", "code": 40006}), 400
    except OrganisationCreationException as e:
        return jsonify({"error": "Issue creating organisation due to mongo reasons", "code": 50002}), 500


@blueprint.route('', methods=['GET'])
def get_organisations():
    try:
        organisations = manager.get_organisations_for_user(g.user_id)
        return jsonify(organisations)
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50003}), 500


@blueprint.route('/<string:org_id>', methods=['GET'])
def get_organisation(org_id: str):
    try:
        organisation = manager.get_organisation_for_user(org_id, g.user_id)
        return jsonify(organisation)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40401}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40101}), 401
