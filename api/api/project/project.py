from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.project import manager
from api.project.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException
from api.commons.common import UnknownSystemException


blueprint = Blueprint('project', __name__, url_prefix='/organisations/<string:org_id>/projects')


@blueprint.route('', methods=['POST'])
def create_project(org_id: str):
    try:
        create_project_request = manager.ProjectRequest(**request.json)
        create_project_response = manager.create_project(org_id, g.user_id, create_project_request)
        return jsonify(create_project_response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40007}), 400
    except DuplicateProjectNameException as e:
        current_app.logger.error('Duplicate name for project')
        return jsonify({"error": f"Duplicate name for project: {e.name}", "code": 40008}), 400
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40407}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40104}), 401


@blueprint.route('', methods=['GET'])
def get_projects(org_id: str):
    try:
        projects = manager.get_projects(org_id, g.user_id)
        projects_dict = list(map(lambda p: p.dict(), projects))
        return jsonify(projects_dict)
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40408}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40105}), 401
    except UnknownSystemException as ex:
        current_app.logger.error("Unknown system exception", ex)
        return jsonify({"error": "Unknown system exception", "code": 50007}), 500
