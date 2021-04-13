from flask import Blueprint, current_app, request, jsonify, escape, g
from pydantic import ValidationError

from api.organisation import manager


blueprint = Blueprint('organisation', __name__, url_prefix='/organisations')


@blueprint.route('/test', methods=['GET'])
def test():
    current_app.logger.info(f'at request.. {g.user_id}')
    return jsonify({"message": "testing before_request"})
