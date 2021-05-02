from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.project import manager
from api.project.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException,\
    OrganisationNotFoundException
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
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40407}), 404
    except DuplicateProjectNameException as e:
        current_app.logger.error('Duplicate name for project')
        return jsonify({"error": f"Duplicate name for project: {e.name}", "code": 40008}), 400
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40408}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40104}), 401


@blueprint.route('', methods=['GET'])
def get_projects(org_id: str):
    try:
        projects = manager.get_projects(org_id, g.user_id)
        projects_dict = list(map(lambda p: p.dict(), projects))
        return jsonify(projects_dict)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40409}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40410}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40105}), 401
    except UnknownSystemException as ex:
        current_app.logger.error("Unknown system exception", ex)
        return jsonify({"error": "Unknown system exception", "code": 50007}), 500


@blueprint.route('/<string:proj_id>', methods=["GET"])
def get_project(org_id: str, proj_id: str):
    try:
        project = manager.get_project(org_id, g.user_id, proj_id)
        return jsonify(project.dict())
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40411}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40412}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40106}), 401
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40410}), 404


@blueprint.route('/<string:proj_id>', methods=['PUT'])
def edit_project(org_id: str, proj_id: str):
    try:
        edit_project_request = manager.ProjectModel(**request.json)
        project = manager.edit_project(org_id, g.user_id, proj_id, edit_project_request)
        return jsonify(project.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with json body')
        return jsonify({"error": "Issue creating project", "code": 40008}), 400
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40413}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40414}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40107}), 401
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40415}), 404
    except UnknownSystemException as ex:
        current_app.logger.error("Unknown system exception", ex)
        return jsonify({"error": "Unknown system exception", "code": 50008}), 500


@blueprint.route('/<string:proj_id>', methods=['DELETE'])
def delete_project(org_id: str, proj_id: str):
    try:
        delete_project_response = manager.delete_project(org_id, g.user_id, proj_id)
        return jsonify(delete_project_response)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40416}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40417}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40418}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40108}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50009}), 500


@blueprint.route('/<string:proj_id>/keys', methods=['POST'])
def create_key(org_id: str, proj_id: str):
    try:
        create_key_response = manager.create_key(org_id, g.user_id, proj_id, manager.KeyRequest(**request.json))
        return create_key_response.dict()
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40419}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40420}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40421}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40109}), 401
    except DuplicateKeyNameException as ex:
        return jsonify({"error": f"Duplicate key name in project {ex.name}", "code": 40009}), 400
    except DuplicateKeyException as ex:
        current_app.logger.error(f"This should really not happen. big trouble. duplicate key: {ex.key}")
        return jsonify({"error": "Duplicate key", "code": 50010}), 500
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50011}), 500


@blueprint.route('/<string:proj_id>/keys', methods=['GET'])
def get_keys(org_id: str, proj_id: str):
    try:
        get_keys_response = manager.get_keys(org_id, g.user_id, proj_id)
        response = list(map(lambda key: key.dict(), get_keys_response))
        return jsonify(response)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40422}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40423}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40424}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40110}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50012}), 500


@blueprint.route('/<string:proj_id>/keys/<string:key_id>', methods=['GET'])
def get_key(org_id: str, proj_id: str, key_id: str):
    try:
        response = manager.get_key(org_id, g.user_id, proj_id, key_id)
        return jsonify(response.dict())
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40425}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40426}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40427}), 404
    except DeletedKeyAccessException as ex:
        current_app.logger.warn(f"Accessing deleted key: {ex.key_id}")
        return jsonify({"error": f"Accessing deleted key by id {ex.key_id}", "code": 40428}), 404
    except KeyNotFoundException as ex:
        current_app.logger.warn(f'Unknown key: {ex.key_id}')
        return jsonify({"error": f"Unknown key by id {ex.key_id}", "code": 40429}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40111}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50013}), 500


@blueprint.route('/<string:proj_id>/keys/<string:key_id>', methods=['PUT'])
def edit_key(org_id: str, proj_id: str, key_id: str):
    try:
        edit_key_request = manager.KeyRequest(**request.json)
        edit_key_response = manager.edit_key(org_id, g.user_id, proj_id, key_id, edit_key_request)
        return edit_key_response.dict()
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40430}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40431}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40432}), 404
    except DeletedKeyAccessException as ex:
        return jsonify({"error": f"Key has been deleted {ex.key_id}", "code": 40433}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40112}), 401
    except DuplicateKeyNameException as ex:
        return jsonify({"error": f"Duplicate key name in project {ex.name}", "code": 40010}), 400
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50012}), 500


@blueprint.route('/<string:proj_id>/keys/<string:key_id>', methods=['DELETE'])
def delete_key(org_id: str, proj_id: str, key_id: str):
    try:
        delete_response = manager.delete_key(org_id, g.user_id, proj_id, key_id)
        return jsonify(delete_response)
    except OrganisationNotFoundException as ex:
        current_app.logger.warn(f"Unknown organisation: {org_id}")
        return jsonify({"error": f"Unknown organisation by id: {org_id}", "code": 40434}), 404
    except DeletedOrganisationAccessException as ex:
        current_app.logger.warn(f"Access to deleted organisation: {org_id}")
        return jsonify({"error": "Accessing deleted organisations", "code": 40435}), 404
    except ProjectNotFoundException as ex:
        current_app.logger.warn(f"Unknown project: {ex.proj_id}")
        return jsonify({"error": f"Unknown project by id {ex.proj_id}", "code": 40436}), 404
    except KeyNotFoundException as ex:
        current_app.logger.warn(f"Unknown key: {ex.key_id}")
        return jsonify({"error": f"Unknown key by id {ex.key_id}", "code": 40437}), 404
    except DeletedKeyAccessException as ex:
        return jsonify({"error": f"Key already deleted {ex.key_id}", "code": 40438}), 404
    except OrganisationIllegalAccessException as ex:
        current_app.logger.warn(f"Unauthorized access: {org_id} by {g.user_id}")
        return jsonify({"error": "No access to organisation", "code": 40113}), 401
    except UnknownSystemException as e:
        return jsonify({"error": "Unknown system exceptions", "code": 50013}), 500
