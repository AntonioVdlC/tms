import os

from flask import Flask, jsonify
from api.db import init_db
from api.cache import init_cache

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_envvar('CONFIG_FILE_PATH')

    # init_db()
    # init_cache()

    @app.route("/ping")
    def ping():
        print(app.config['REDIS_HOST'])
        return jsonify({"message": "pong"})

    return app