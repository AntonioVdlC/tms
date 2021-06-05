from flask import Blueprint, current_app, request, jsonify, escape
from pydantic import ValidationError

from api.auth import manager
from api.auth.exceptions import *
from api.commons import common as common
from api.commons import codes

blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        signup_request = manager.SignupRequest(**request.json)
        signup_request.first_name = str(escape(signup_request.first_name))
        signup_request.last_name = str(escape(signup_request.last_name))
        signup_response = manager.signup(signup_request)
        return jsonify(signup_response)
    except ValidationError as e:
        current_app.logger.error('Issue with the json body')
        return jsonify({"error": "Invalid user params", "code": codes.INVALID_JSON}), 400
    except DuplicateSignupException as e:
        current_app.logger.warn(f'Duplicate sign up request for {e.email}')
        return jsonify({"error": f"User already exists for email {e.email}", "code": codes.DUPLICATE_EMAIL}), 400
    except common.UnknownAuthException as e:
        current_app.logger.error('Redis connection error')
        return jsonify({"error": "Unknown error", "code": codes.UNKNOWN_AUTH_EXCEPTION}), 500


@blueprint.route('/login', methods=['POST'])
def login():
    current_app.logger.info('Logging in user..')
    try:
        login_request = manager.LoginRequest(**request.json)
        login_response = manager.login(login_request)
        return jsonify(login_response)
    except ValidationError as e:
        current_app.logger.error('Issue with the json body')
        return jsonify({"error": "Incorrect email address", "code": codes.INVALID_JSON}), 400
    except UnknownEmailException as e:
        current_app.logger.warn(f'No user found for email: {e.email}')
        return jsonify({"error": f"No user found for email: {e.email}. Please sign up first",
                        "code": codes.UNKNOWN_EMAIL}), 400
    except common.UnknownAuthException as e:
        current_app.logger.error('Connection error with redis/mongo')
        return jsonify({"error": "Unknown error", "code": codes.UNKNOWN_AUTH_EXCEPTION}), 500


@blueprint.route('/callback', methods=['POST'])
def callback():
    current_app.logger.info('Callback for auth')
    try:
        callback_request = manager.CallbackRequest(**request.json)
        callback_response = manager.callback(callback_request)
        response = jsonify({"message": "you are in homer"})
        access_token = f'Bearer {callback_response.token}'
        if current_app.config['ENV'] == 'development':
            current_app.logger.info("env is development")
            response.set_cookie('access_token', access_token)
        else:
            response.set_cookie('access_token', access_token, secure=True, httponly=True)
        return response
    except ValidationError as e:
        return jsonify({"error": "Illegal json parameters", "code": codes.INVALID_JSON}), 400
    except InvalidTokenException as e:
        return jsonify({"error": f"Invalid token: {e.token}", "code": codes.INVALID_TOKEN}), 400
    except DuplicateSignupException as e:
        current_app.logger.warn(f'Duplicate sign up request for {e.email}')
        return jsonify({"error": f"User already exists for email {e.email}. Please try logging in",
                        "code": codes.DUPLICATE_EMAIL}), 400
    except InvalidOperationException as e:
        current_app.logger.warn('Invalid operation in request')
        return jsonify({"error": e.msg, "code": codes.INVALID_AUTH_CALLBACK}), 400
    except common.UnknownAuthException as e:
        current_app.logger.error('Connection error with redis/mongo')
        return jsonify({"error": "Unknown error", "code": codes.UNKNOWN_AUTH_EXCEPTION}), 500


@blueprint.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.cookies.get('access_token').split()[1]
        manager.logout(token)
        response = jsonify({"message": "Logged out user"})
        response.delete_cookie('access_token')
        return response
    except AttributeError as e:
        return jsonify({"message": "Missing Authorization header", "code": codes.MISSING_AUTH_HEADER}), 401
    except IndexError as e:
        return jsonify({"message": "Illegal token format", "code": codes.ILLEGAL_TOKEN_FORMAT}), 400
    except common.UnknownAuthException as e:
        return jsonify({"message": "Redis connection issue", "code": codes.UNKNOWN_AUTH_EXCEPTION}), 500
