from flask import Blueprint, current_app, request, jsonify
from pydantic import ValidationError

from api.auth import manager


blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@blueprint.route('/login', methods=['POST'])
def login():
    current_app.logger.info('Logging in user..')
    try:
        login_request = manager.LoginRequest(**request.json)
        login_response = manager.login(login_request)
        return jsonify(login_response.dict())
    except ValidationError as e:
        current_app.logger.error('Issue with the json body')
        return jsonify({"error": "Incorrect email address"}), 400
