from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.organisation import manager


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
        return jsonify({"error": f"Issue creating organisation with given name", "code": 40006}), 400
