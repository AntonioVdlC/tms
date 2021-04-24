from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.project import manager
from api.project.exceptions import *


blueprint = Blueprint('project', __name__, url_prefix='/organisations/<string:org_id>/projects')


@blueprint.route('', methods=['GET'])
def get_projects(org_id: str):
    return jsonify({"organisation": org_id})


@blueprint.route('/<string:proj_id>', methods=['GET'])
def get_project(org_id: str, proj_id: str):
    return jsonify({"organisation": org_id, "project": proj_id})
