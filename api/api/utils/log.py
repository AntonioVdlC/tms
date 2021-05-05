import logging

from flask import has_request_context, request, current_app
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.full_path = request.full_path
            record.remote_addr = request.remote_addr
        else:
            record.full_path = None
            record.remote_addr = None

        return super().format(record)


def init_log():
    formatter = RequestFormatter(
        '[%(asctime)s] %(module)s %(levelname)s: %(message)s'
    )
    default_handler.setFormatter(formatter)

