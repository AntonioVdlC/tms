from flask import Blueprint, current_app
from api.utils.db import get_db
from api.utils.cache import get_cache

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/login', methods=['POST'])
def login():
    current_app.logger.info('Logging in user..')
    return {"status": "logged in"}