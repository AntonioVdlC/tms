from flask import Flask, jsonify
from api.utils.cache import init_cache, get_cache
from api.utils.db import init_db, get_db
from api.utils.log import init_log


def create_app(test_config=None):
    init_log()

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_envvar('CONFIG_FILE_PATH')

    with app.app_context():
        init_cache()
        init_db()

    @app.route("/ping")
    def ping():
        app.logger.info(get_cache().ping())
        app.logger.info(get_db().tms.command('ping'))
        return jsonify({"message": "pong"})

    return app
