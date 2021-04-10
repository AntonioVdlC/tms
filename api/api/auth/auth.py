from flask import Blueprint, current_app, request, jsonify
from pydantic import ValidationError

from api.auth import manager
from api.auth.exceptions import DuplicateSignupException, UnknownEmailException

blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        signup_request = manager.SignupRequest(**request.json)
        signup_response = manager.signup(signup_request)
        return jsonify(signup_response)
    except ValidationError as e:
        current_app.logger.error('Issue with the json body')
        return jsonify({"error": "Incorrect email address", "code": 40001}), 400
    except DuplicateSignupException as e:
        current_app.logger.warn(f'Duplicate sign up request for {e.email}')
        return jsonify({"error": f"User already exists for email {e.email}", "code": 40002}), 400


@blueprint.route('/login', methods=['POST'])
def login():
    current_app.logger.info('Logging in user..')
    try:
        login_request = manager.LoginRequest(**request.json)
        login_response = manager.login(login_request)
        return jsonify(login_response)
    except ValidationError as e:
        current_app.logger.error('Issue with the json body')
        return jsonify({"error": "Incorrect email address", "code": 40001}), 400
    except UnknownEmailException as e:
        current_app.logger.warn(f'No user found for email: {e.email}')
        return jsonify({"error": f"No user found for email: {e.email}. Please sign up first", "code": 40003}), 400


@blueprint.route('/callback', methods=['POST'])
def callback():
    current_app.logger.info('Callback for auth')
    try:
        callback_request = manager.CallbackRequest(**request.json)
        callback_response = manager.callback(callback_request)
        return jsonify(callback_response.dict())
    except ValidationError as e:
        return jsonify({"error": "error in json", "code": 40004}), 400
