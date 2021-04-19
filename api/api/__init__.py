from flask import Flask, jsonify, g, current_app, request
from api.utils.cache import init_cache, get_cache
from api.utils.db import init_db, get_db
from api.utils.log import init_log
from api.auth import auth
from api.organisation import organisation


def create_app(test_config=None):
    init_log()

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_envvar('CONFIG_FILE_PATH')

    with app.app_context():
        init_cache()
        init_db()

    def before_request_auth():
        try:
            token = request.cookies.get('access_token').split()[1]
            user_id = get_cache().get(token)
            if user_id is None:
                return jsonify({"message": "Token expired"}), 401
            g.user_id = user_id
        except (AttributeError, IndexError) as e:
            return jsonify({"message": "Not logged in"}), 401

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(organisation.blueprint)
    app.before_request_funcs = {
        'organisation': [before_request_auth]
    }

    @app.route("/ping")
    def ping():
        app.logger.info(get_cache().ping())
        app.logger.info(get_db().command('ping'))
        return jsonify({"message": "pong"})

    return app
